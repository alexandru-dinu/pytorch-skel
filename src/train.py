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

    dump_cfg(f"{base_dir}/train_config.txt", vars(cfg))


def epilogue(cfg: Namespace, *varargs) -> None:
    pass


def train(cfg: Namespace) -> None:
    logger.info("=== Training ===")

    # initial setup
    prologue(cfg)

    # TODO: train-related code
    model = ...
    dataset = ...
    dataloader = ...

    optimizer = ...
    loss_criterion = ...
    scheduler = ...

    # train-loop
    for epoch_idx in range(cfg.start_epoch, cfg.num_epochs + 1):

        # scheduler.step()

        for batch_idx, data in enumerate(dataloader, start=1):
            # forward pass
            loss = ...
            # optimizer

            logger.debug(
                '[%3d/%3d][%5d/%5d] avg_loss: %.8f' %
                (epoch_idx, cfg.num_epochs, batch_idx, len(dataloader), loss)
            )

            if batch_idx % cfg.batch_every:
                # TODO: do some reporting every N batches: out, running average etc
                pass
        # -- batch-loop

        if epoch_idx % cfg.epoch_every:
            # TODO: do some reporting every N epochs: save, average etc
            pass

    # -- train-loop

    # save final model
    torch.save(model.state_dict(), f"../experiments/{cfg.exp_name}/model_final.pth")

    # final setup
    epilogue(cfg)


if __name__ == '__main__':
    args = get_args()
    config = get_config(args)

    train(config)
