from freq_math import forward_wavelet_packet_transform, calculate_frechet_distance
import torch as th
import os
from typing import List, Tuple
from PIL import Image
from torchvision.transforms import functional as TVF
import torchvision.transforms as TV
import numpy as np
import pathlib
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from tqdm import tqdm

th.set_default_dtype(th.float64)
# from multiprocessing import Pool


parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--batch-size", type=int, default=128, help="Batch size for wavelet packet transform.")
parser.add_argument("--num-processes", type=int, default=None, help="Number of multiprocess.")
parser.add_argument("--save-packets", action="store_true", help="Save the packets as npz file.")
parser.add_argument("--wavelet", type=str, default="sym5", help="Choice of wavelet.")
parser.add_argument("--max_level", type=int, default=4, help="wavelet decomposition level")
parser.add_argument("--log_scale", action="store_false", help="Use log scaling for wavelets.")
parser.add_argument("path", type=str, nargs=2, help="Path to the generated images or path to .npz statistics file.")

IMAGE_EXTS = {"jpg", "jpeg", "png"}
NUM_PROCESSES = None


class ImagePathDataset(th.utils.data.Dataset):
    def __init__(self, files, transforms=None):
        self.files = files
        self.transforms = transforms

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        path = self.files[i]
        img = Image.open(path).convert("RGB")
        if self.transforms is not None:
            img = self.transforms(img)
        return img
# def read_image(img_name):
#     return TVF.pil_to_tensor(Image.open(img_name).convert("RGB"))/255.


def packet_transform(
        dataloader: th.utils.data.DataLoader,
        wavelet: str,
        max_level: int,
        log_scale: bool
) -> th.Tensor:
    """Compute wavelet packet transform across batches.

    Args:
        imgs (List[str]): List containing batched images.
        wavelet (str): Choice of wavelet.
        max_level (int): Wavelet decomposition level.
        log_scale (bool): Apply log scale.

    Returns:
        th.Tensor: Packets of shape [BS, P, C, H_n, W_n].
    """
    packets = []
    device = th.device('cuda:0') if th.cuda.is_available() else th.device('cpu')
    for img_batch in tqdm(dataloader):
        # image = [read_image(nm) for nm in img_batch]
        # # with Pool(NUM_PROCESSES) as p:
        # #     image = p.map(read_image, img_batch)
        # tensor_ = th.stack(image, dim=0)
        img_batch = img_batch.to(device)
        packets.append(
            forward_wavelet_packet_transform(
                img_batch,
                wavelet,
                max_level,
                log_scale
            ).cpu()
        )
    packet_tensor = th.cat(packets, dim=0)
    packet_tensor = th.permute(packet_tensor, (1, 0, 2, 3, 4))
    P, BS, C, H, W = packet_tensor.shape
    return th.reshape(packet_tensor, (P, BS, C*H*W))


def compute_statistics(
        dataloader: th.utils.data.DataLoader,
        wavelet: str,
        max_level: int,
        log_scale: bool
) -> Tuple[np.ndarray, ...]:
    """Calculate mean and standard deviation across packets.

    Args:
        img_names (List[str]): List of image file names.
        wavelet (str): Choice of wavelet.
        max_level (int): Wavelet decomposition level.
        log_scale (bool): Apply log scale.
        batch_size (int): Batch size for tensor split.

    Returns:
        Tuple[th.Tensor, th.Tensor]: tuple containing mean and std for each packet.
    """
    packets = packet_transform(dataloader, wavelet, max_level, log_scale)
    print('Computing mean and std for each packet.')
    # packets = packets.numpy()
    # mu = np.mean(packets, axis=1)
    # sigma = np.array([np.cov(packets[p, :, :], rowvar=False) for p in tqdm(range(len(packets)))])
    mu = th.mean(packets, dim=1).numpy()
    sigma = th.stack([th.cov(packets[p, :, :].T) for p in range(len(packets))], dim=0).numpy()
    return mu, sigma


def calculate_path_statistics(path:str, wavelet: str, max_level: int, log_scale: bool, batch_size: int) -> Tuple[np.ndarray, ...]:
    """Compute mean and sigma for given path.

    Args:
        path (str): npz path or image directory.
        wavelet (str): Choice of wavelet.
        max_level (int): Decomposition level.
        log_scale (bool): Apply log scale.
        batch_size (int): Batch size for packet decomposition.

    Raises:
        ValueError: Error if mu and sigma cannot be calculated.

    Returns:
        Tuple[np.ndarray, ...]: Tuple containing mean and sigma for each packet.
    """
    mu, sigma = None, None
    if path.endswith(".npz"):
        with np.load(path) as fp:
            mu = fp["mu"][:]
            sigma = fp["sigma"][:]
    else:
        path = pathlib.Path(path)
        img_names = sorted(
            [
                name
                for ext in IMAGE_EXTS
                for name in path.glob(f"*.{ext}")
            ]
        )
        dataloader = th.utils.data.DataLoader(
            ImagePathDataset(img_names, transforms=TV.ToTensor()),
            batch_size=batch_size,
            shuffle=False,
            drop_last=False,
            num_workers=NUM_PROCESSES
        )
        mu, sigma = compute_statistics(
            dataloader=dataloader,
            wavelet=wavelet,
            max_level=max_level,
            log_scale=log_scale
        )
    
    if (mu is None) or (sigma is None):
        raise ValueError(f"The file path: {path} is empty/doesn't have statistics.")
    return mu, sigma


def compute_fwd(paths: List[str], wavelet: str, max_level: int, log_scale: bool, batch_size: int) -> float:
    """Compute Frechet Wavelet Distance.

    Args:
        paths (List[str]): List containing path of source and generated images.
        wavelet (str): Choice of wavelet.
        max_level (int): Decomposition level.
        log_scale (bool): Apply log scale.
        batch_size (int): Batch size for packet decomposition.

    Raises:
        RuntimeError: Error if path doesn't exist.

    Returns:
        float: Frechet Wavelet Distance.
    """
    for path in paths:
        if not os.path.exists(path):
            raise RuntimeError(f"Invalid path: {path}")
    
    print(f"Computing stats for path: {paths[0]}")
    mu_1, sigma_1 = calculate_path_statistics(paths[0], wavelet, max_level, log_scale, batch_size)
    print(f"Computing stats for path: {paths[1]}")
    mu_2, sigma_2 = calculate_path_statistics(paths[1], wavelet, max_level, log_scale, batch_size)

    frechet_distances = []
    print("Computing Frechet distances for each packet.")
    for packet_no in tqdm(range(len(mu_1))):
        fd = calculate_frechet_distance(mu1=mu_1[packet_no, :], mu2=mu_2[packet_no, :],
                                        sigma1=sigma_1[packet_no, :, :], sigma2=sigma_2[packet_no, :, :])
        frechet_distances.append(fd)
    return np.mean(frechet_distances)


def save_packets(paths: List[str], wavelet: str, max_level:int, log_scale: bool, batch_size: int) -> None:
    """Save packets.

    Args:
        paths (List[str]): List of paths containing input and output files.
        wavelet (str): Choice of wavelet.
        max_level (int): Decomposition level.
        log_scale (bool): Apply log scale.
        batch_size (int): Batch size for packet decomposition.

    Raises:
        RuntimeError: Error if input path is invalid.
        RuntimeError: Error if the output file already exists.
    """
    if not os.path.exists(paths[0]):
        raise RuntimeError(f"Invalid path: {paths[0]}")
    
    if os.path.exists(paths[1]):
        raise RuntimeError(f"Stats file already exists at the given path: {paths[1]}")
    
    print(f"Computing stats for path: {paths[0]}")
    mu_1, sigma_1 = calculate_path_statistics(paths[0], wavelet, max_level, log_scale, batch_size)
    np.savez_compressed(paths[1], mu=mu_1, sigma=sigma_1)


def main():
    global NUM_PROCESSES, IMAGE_EXTS

    args = parser.parse_args()
    if args.num_processes is None:
        try:
            num_cpus = len(os.sched_getaffinity(0))
        except AttributeError:
            num_cpus = os.cpu_count()
        NUM_PROCESSES = min(num_cpus, 16) if num_cpus is not None else 0
    else:
        NUM_PROCESSES = args.num_processes
    print(f'Num work: {NUM_PROCESSES}')
    if args.save_packets:
        save_packets(args.path, args.wavelet, args.max_level, args.log_scale, args.batch_size)
        return
    
    fwd = compute_fwd(args.path, args.wavelet, args.max_level, args.log_scale, args.batch_size)
    print(f"FWD: {fwd}")


if __name__ == '__main__':
    main()
