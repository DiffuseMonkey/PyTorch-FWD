"""Config for CelebA and CelebHQ datasets."""

from dataclasses import dataclass
from typing import Dict, Any, Union

celeba_path: Union[str, None] = '<path_to_celeba_dataset>'
celebahq_path: Union[str, None] = '<path_to_celebahq_dataset>'


@dataclass
class CelebA64():
    dataset: Dict[str, Any] = {
        'random_flip': True,
        'num_workers': 48, # Feel free to change this
        'dataset': 'CELEBA',
        'resize': 64,
    }

    model: Dict[str, Any] = {
        'in_c': 3,
        'out_c': 3,
        'model_c': 128,
        'num_res_blocks': 2,
        'attn_res': tuple([16]),
        'dropout': 0.0,
        'channel_mult': tuple([1, 2, 2, 2, 4]),
        'num_classes': 1000,
        'num_heads': 4,
        'num_heads_ups': 4,
        'use_scale_shift_norm': True,
        'input_size': 64
    }

    optimizer: Dict[str, Any] = {
        'lr': 2e-4,
        'grad_clip_norm': 1.0  # TODO: Check this again.
    }

    data_dir: Union[str, None] = celeba_path


@dataclass
class CelebAHQ64():
    dataset: Dict[str, Any] = {
        'random_flip': True,
        'num_workers': 48, # Feel free to change this
        'dataset': 'CELEBAHQ',
        'resize': 64,
    }

    model: Dict[str, Any] = {
        'in_c': 3,
        'out_c': 3,
        'model_c': 128,
        'num_res_blocks': 2,
        'attn_res': tuple([16, 8]),
        'dropout': 0.0,
        'channel_mult': tuple([1, 2, 2, 4]),
        'num_classes': 1000,
        'num_heads': 4,
        'num_heads_ups': 4,
        'use_scale_shift_norm': True,
        'input_size': 64
    }

    optimizer: Dict[str, Any] = {
        'lr': 1e-4,
        'grad_clip_norm': 1.0  # TODO: Check this again.
    }

    data_dir: Union[str, None] = celebahq_path


@dataclass
class CelebAHQ128():
    dataset: Dict[str, Any] = {
        'random_flip': True,
        'num_workers': 48, # Feel free to change this
        'dataset': 'CELEBAHQ',
        'resize': 128,
    }

    model: Dict[str, Any] = {
        'in_c': 3,
        'out_c': 3,
        'model_c': 128,
        'num_res_blocks': 3,
        'attn_res': tuple([16, 8]),
        'dropout': 0.0,
        'channel_mult': tuple([1, 2, 2, 4, 4]),
        'num_classes': 1000,
        'num_heads': 4,
        'num_heads_ups': 4,
        'use_scale_shift_norm': True,
        'input_size': 128
    }

    optimizer: Dict[str, Any] = {
        'lr': 1e-4,
        'grad_clip_norm': 1.0  # TODO: Check this again.
    }

    data_dir: Union[str, None] = celebahq_path