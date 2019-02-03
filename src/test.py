import os
from argparse import Namespace

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

import logger
from utils import get_config, get_args, dump_cfg


def prologue(cfg: Namespace, *varargs) -> None:
    base_dir = f"../experiments/{cfg.exp_name}"

    os.makedirs(f"{base_dir}/out", exist_ok=True)
    os.makedirs(f"{base_dir}/chkpt", exist_ok=True)

    dump_cfg(f"{base_dir}/test_config.txt", vars(cfg))


def epilogue(cfg: Namespace, *varargs) -> None:
    pass


def test(cfg: Namespace) -> None:
    logger.info("=== Testing ===")

    # initial setup
    prologue(cfg)

    model = ...
    dataset = ...
    dataloader = ...

    for batch_idx, data in enumerate(dataloader, start=1):
        pass

    # final setup
    epilogue(cfg)


if __name__ == '__main__':
    args = get_args()
    config = get_config(args)

    test(config)
