"""Config for CelebA and CelebHQ datasets."""

from typing import Any, Dict

celeba_path: str = None
celebahq_path: str = None


class CELEBA64:
    def __init__(self) -> None:
        self.dataset_config: Dict[str, Any] = {
            "random_flip": True,
            "num_workers": 48,  # Feel free to change this
            "dataset": "CELEBA",
            "resize": 64,
            "mean": [x / 255.0 for x in [129.058, 108.485, 97.622]],
            "std": [x / 255.0 for x in [78.338, 73.131, 72.970]],
        }

        self.model_config: Dict[str, Any] = {
            "in_c": 3,
            "out_c": 3,
            "model_c": 128,
            "num_res_blocks": 2,
            "attn_res": tuple([16]),
            "dropout": 0.0,
            "channel_mult": tuple([1, 2, 2, 2, 4]),
            "num_classes": 1000,
            "num_heads": 4,
            "num_heads_ups": 4,
            "use_scale_shift_norm": True,
            "input_size": 64,
        }

        self.optimizer_config: Dict[str, Any] = {
            "lr": 2e-4,
            "clip_grad_norm": 1.0,  # TODO: Check this again.
        }

        self.data_dir: str = celeba_path


class CELEBAHQ64:
    def __init__(self) -> None:
        self.dataset_config: Dict[str, Any] = {
            "random_flip": True,
            "num_workers": 48,  # Feel free to change this
            "dataset": "CELEBAHQ",
            "resize": 64,
            "mean": [x / 255.0 for x in [131.810, 106.258, 92.634]],
            "std": [x / 255.0 for x in [76.332, 69.183, 67.954]],
        }

        self.model_config: Dict[str, Any] = {
            "in_c": 3,
            "out_c": 3,
            "model_c": 128,
            "num_res_blocks": 2,
            "attn_res": tuple([16, 8]),
            "dropout": 0.0,
            "channel_mult": tuple([1, 2, 2, 4]),
            "num_classes": 6217,
            "num_heads": 4,
            "num_heads_ups": 4,
            "use_scale_shift_norm": True,
            "input_size": 64,
        }

        self.optimizer_config: Dict[str, Any] = {
            "lr": 1e-4,
            "clip_grad_norm": 1.0,  # TODO: Check this again.
        }

        self.data_dir: str = celebahq_path


class CELEBAHQ128:
    def __init__(self) -> None:
        self.dataset_config: Dict[str, Any] = {
            "random_flip": True,
            "num_workers": 48,  # Feel free to change this
            "dataset": "CELEBAHQ",
            "resize": None,
            "mean": [x / 255.0 for x in [131.810, 106.258, 92.634]],
            "std": [x / 255.0 for x in [76.332, 69.183, 67.954]],
        }

        self.model_config: Dict[str, Any] = {
            "in_c": 3,
            "out_c": 3,
            "model_c": 128,
            "num_res_blocks": 3,
            "attn_res": tuple([16, 8]),
            "dropout": 0.0,
            "channel_mult": tuple([1, 2, 2, 4, 4]),
            "num_classes": 6217,
            "num_heads": 4,
            "num_heads_ups": 4,
            "use_scale_shift_norm": True,
            "input_size": 128,
        }

        self.optimizer_config: Dict[str, Any] = {
            "lr": 1e-4,
            "clip_grad_norm": 1.0,  # TODO: Check this again.
        }

        self.data_dir: str = celebahq_path

        self.norm_weights = {
            "haar_l3": [
                0.18777889013290405,
                0.9710429906845093,
                0.9707638621330261,
                0.9931913614273071,
                0.9864241480827332,
                0.9870322942733765,
                0.9970768094062805,
                0.9960458874702454,
                0.9855464100837708,
                0.9967818260192871,
                0.994523823261261,
                0.9954739212989807,
                0.9985864758491516,
                0.9981922507286072,
                0.998842716217041,
                0.9990741610527039,
                0.9933870434761047,
                0.9941969513893127,
                0.9986422061920166,
                0.9984362721443176,
                0.9984094500541687,
                0.9981328248977661,
                0.9993311166763306,
                0.9989345073699951,
                0.9993430376052856,
                0.9992878437042236,
                0.9994747042655945,
                0.9996297359466553,
                0.9996768832206726,
                0.9994822144508362,
                0.9979738593101501,
                0.9979062080383301,
                0.9931361079216003,
                0.9985382556915283,
                0.9975590109825134,
                0.9980301856994629,
                0.9993646740913391,
                0.9990947842597961,
                0.9994685053825378,
                0.9995315670967102,
                0.997765302658081,
                0.9985148906707764,
                0.9987520575523376,
                0.999146044254303,
                0.9995391964912415,
                0.9992204904556274,
                0.9997932314872742,
                0.9995009899139404,
                0.9996944069862366,
                0.9996473789215088,
                0.9997705817222595,
                0.999836802482605,
                0.999863862991333,
                0.999751627445221,
                0.9991602301597595,
                0.9990562796592712,
                0.9999058842658997,
                0.9997252821922302,
                0.9998801946640015,
                0.9997596740722656,
                0.9994721412658691,
                0.9992935657501221,
                0.9998179078102112,
                0.9997860789299011,
            ],
            "haar_l2": [
                0.0800747275352478,
                0.9780480861663818,
                0.9814229607582092,
                0.9969100952148438,
                0.9897764325141907,
                0.9968819618225098,
                0.9986848831176758,
                0.9966328144073486,
                0.9913052320480347,
                0.9985143542289734,
                0.996516227722168,
                0.9988073706626892,
                0.9993835687637329,
                0.998535692691803,
                0.9995526075363159,
                0.998953104019165,
            ],
            "db2_l2": [
                0.03834044933319092,
                0.9883729815483093,
                0.9925981760025024,
                0.9972652196884155,
                0.9974744319915771,
                0.9964457750320435,
                0.9991838932037354,
                0.9986961483955383,
                0.998141884803772,
                0.9994933009147644,
                0.9967793822288513,
                0.9986762404441833,
                0.999838650226593,
                0.9998192191123962,
                0.9995104670524597,
                0.9993636608123779,
            ],
            "db2_l3": [
                0.10848993062973022,
                0.9738131761550903,
                0.9853153824806213,
                0.995220959186554,
                0.9928703904151917,
                0.9934724569320679,
                0.998015284538269,
                0.9969393610954285,
                0.9960914850234985,
                0.99883633852005,
                0.9957753419876099,
                0.9969750642776489,
                0.9993109107017517,
                0.9990206360816956,
                0.9989132285118103,
                0.9982315301895142,
                0.998688280582428,
                0.9984326362609863,
                0.9997441172599792,
                0.999107837677002,
                0.9989015460014343,
                0.9977681636810303,
                0.9984432458877563,
                0.998947262763977,
                0.9998968243598938,
                0.9997488856315613,
                0.9998785853385925,
                0.9993495941162109,
                0.9996901154518127,
                0.999739944934845,
                0.9990999102592468,
                0.9994240999221802,
                0.9987577795982361,
                0.999631941318512,
                0.9991722106933594,
                0.9993965029716492,
                0.9998793601989746,
                0.9997659921646118,
                0.9998008608818054,
                0.9997014403343201,
                0.9985272884368896,
                0.9981991052627563,
                0.9989141821861267,
                0.9988254308700562,
                0.9993411302566528,
                0.9994937181472778,
                0.9994916915893555,
                0.9993698000907898,
                0.9999447464942932,
                0.9999421238899231,
                0.9999526739120483,
                0.9998918771743774,
                0.9999220371246338,
                0.9999322295188904,
                0.9999356865882874,
                0.9998976588249207,
                0.9999099373817444,
                0.9996792674064636,
                0.9999274015426636,
                0.9997396469116211,
                0.9997406005859375,
                0.9997643828392029,
                0.9996375441551208,
                0.9997612833976746,
            ],
            "sym2_l2": [
                0.03834044933319092,
                0.9883729815483093,
                0.9925981760025024,
                0.9972652196884155,
                0.9974744319915771,
                0.9964457750320435,
                0.9991838932037354,
                0.9986961483955383,
                0.998141884803772,
                0.9994933009147644,
                0.9967793822288513,
                0.9986762404441833,
                0.999838650226593,
                0.9998192191123962,
                0.9995104670524597,
                0.9993636608123779,
            ],
            "sym2_l3": [
                0.10848993062973022,
                0.9738131761550903,
                0.9853153824806213,
                0.995220959186554,
                0.9928703904151917,
                0.9934724569320679,
                0.998015284538269,
                0.9969393610954285,
                0.9960914850234985,
                0.99883633852005,
                0.9957753419876099,
                0.9969750642776489,
                0.9993109107017517,
                0.9990206360816956,
                0.9989132285118103,
                0.9982315301895142,
                0.998688280582428,
                0.9984326362609863,
                0.9997441172599792,
                0.999107837677002,
                0.9989015460014343,
                0.9977681636810303,
                0.9984432458877563,
                0.998947262763977,
                0.9998968243598938,
                0.9997488856315613,
                0.9998785853385925,
                0.9993495941162109,
                0.9996901154518127,
                0.999739944934845,
                0.9990999102592468,
                0.9994240999221802,
                0.9987577795982361,
                0.999631941318512,
                0.9991722106933594,
                0.9993965029716492,
                0.9998793601989746,
                0.9997659921646118,
                0.9998008608818054,
                0.9997014403343201,
                0.9985272884368896,
                0.9981991052627563,
                0.9989141821861267,
                0.9988254308700562,
                0.9993411302566528,
                0.9994937181472778,
                0.9994916915893555,
                0.9993698000907898,
                0.9999447464942932,
                0.9999421238899231,
                0.9999526739120483,
                0.9998918771743774,
                0.9999220371246338,
                0.9999322295188904,
                0.9999356865882874,
                0.9998976588249207,
                0.9999099373817444,
                0.9996792674064636,
                0.9999274015426636,
                0.9997396469116211,
                0.9997406005859375,
                0.9997643828392029,
                0.9996375441551208,
                0.9997612833976746,
            ],
        }


class CELEBAHQ256:
    def __init__(self) -> None:
        self.dataset_config: Dict[str, Any] = {
            "random_flip": True,
            "num_workers": 48,  # Feel free to change this
            "dataset": "CELEBAHQ",
            "resize": None,
            "mean": [x / 255.0 for x in [131.810, 106.258, 92.634]],
            "std": [x / 255.0 for x in [76.332, 69.183, 67.954]],
        }

        self.model_config: Dict[str, Any] = {
            "in_c": 3,
            "out_c": 3,
            "model_c": 128,
            "num_res_blocks": 3,
            "attn_res": tuple([16, 8]),
            "dropout": 0.0,
            "channel_mult": tuple([1, 2, 2, 4, 4]),
            "num_classes": 6217,
            "num_heads": 4,
            "num_heads_ups": 4,
            "use_scale_shift_norm": True,
            "input_size": 256,
        }

        self.optimizer_config: Dict[str, Any] = {
            "lr": 1e-4,
            "clip_grad_norm": 1.0,  # TODO: Check this again.
        }

        self.data_dir: str = (
            "/p/scratch/holistic-vid-westai/veeramacheneni2_scratch/CelebAMask-HQ/data256x256/"
        )
