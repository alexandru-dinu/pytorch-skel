import os
import sys
from argparse import Namespace

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import cli_logger
from utils import get_config, get_args, dump_cfg


def prologue(cfg: Namespace, *varargs) -> None:
    # sanity checks
    assert cfg.chkpt not in [None, ""]
    assert cfg.device == "cpu" or (cfg.device == "cuda" and torch.cuda.is_available())

    # dirs
    base_dir = f"../experiments/{cfg.exp_name}"

    os.makedirs(f"{base_dir}/out", exist_ok=True)

    dump_cfg(f"{base_dir}/test_config.txt", vars(cfg))


def epilogue(cfg: Namespace, *varargs) -> None:
    pass


def test(cfg: Namespace) -> None:
    cli_logger.info("=== Testing ===")

    # initial setup
    prologue(cfg)

    model = ...
    model.load_state_dict(torch.load(cfg.chkpt))
    model.eval()
    if cfg.device == "cuda":
        model.cuda()

    cli_logger.info("Loaded model")

    dataset = ...
    dataloader = ...

    cli_logger.info("Loaded data")

    for batch_idx, data in enumerate(dataloader, start=1):
        # ... = data
        if cfg.device == 'cuda':
            # move tensors to cuda
            pass

        if batch_idx % cfg.batch_every == 0:
            pass

    # final setup
    epilogue(cfg)


if __name__ == '__main__':
    args = get_args()
    config = get_config(args)

    test(config)
