import os
import sys
from argparse import Namespace

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from tensorboardX import SummaryWriter

import cli_logger
from utils import get_config, get_args, dump_cfg

# models
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../models"))


def prologue(cfg: Namespace, *varargs) -> SummaryWriter:
    # sanity checks
    assert cfg.device == "cpu" or (cfg.device == "cuda" and torch.cuda.is_available())

    # dirs
    base_dir = f"../experiments/{cfg.exp_name}"

    os.makedirs(f"{base_dir}/out", exist_ok=True)
    os.makedirs(f"{base_dir}/chkpt", exist_ok=True)
    os.makedirs(f"{base_dir}/logs", exist_ok=True)

    dump_cfg(f"{base_dir}/train_config.txt", vars(cfg))

    # tb writer
    writer = SummaryWriter(f"{base_dir}/logs")

    return writer


def epilogue(cfg: Namespace, *varargs) -> None:
    writer = varargs[0]
    writer.close()


def train(cfg: Namespace) -> None:
    cli_logger.info("=== Training ===")

    # initial setup
    writer = prologue(cfg)

    # train-related code
    model = ...
    model.train()
    test_x = torch.rand(...)
    if cfg.device == "cuda":
        model.cuda()
        test_x = test_x.cuda()

    writer.add_graph(model, Variable(test_x, requires_grad=True))
    cli_logger.debug("Model loaded")


    dataset = ...
    dataloader = ...

    cli_logger.debug("Data loaded")


    optimizer = ...
    loss_criterion = ...
    scheduler = ...

    avg_loss, epoch_avg = 0.0, 0.0
    ts = 0

    # train-loop
    for epoch_idx in range(cfg.start_epoch, cfg.num_epochs + 1):

        # scheduler.step()

        for batch_idx, data in enumerate(dataloader, start=1):
            # ... = data
            if cfg.device == "cuda":
                # move tensors to cuda
                pass

            optimizer.zero_grad()
            out = model(...)
            loss = loss_criterion(...)

            # optimizer

            cli_logger.debug(
                '[%3d/%3d][%5d/%5d] avg_loss: %.8f' %
                (epoch_idx, cfg.num_epochs, batch_idx, len(dataloader), loss)
            )

            if batch_idx % cfg.batch_every == 0:
                # do some reporting every N batches: out, running average etc
                writer.add_scalar("train/avg_loss", avg_loss / cfg.batch_every, ts)

                for name, param in model.named_parameters():
                    writer.add_histogram(name, param, ts)

                cli_logger.debug(
                    '[%3d/%3d][%5d/%5d] avg_loss: %.8f' %
                    (epoch_idx, cfg.num_epochs, batch_idx, len(dataloader), avg_loss / cfg.batch_every)
                )
                avg_loss = 0.0
                ts += 1

        # -- batch-loop

        if epoch_idx % cfg.epoch_every == 0:
            cli_logger.info("Epoch avg = %.8f" % (epoch_avg / (len(dataloader) * cfg.epoch_every)))
            epoch_avg = 0.0
            torch.save(model.state_dict(), f"../experiments/{cfg.exp_name}/chkpt/model_{epoch_idx}.pth")
    # -- train-loop

    # save final model
    torch.save(model.state_dict(), f"../experiments/{cfg.exp_name}/model_final.pth")

    # final setup
    epilogue(cfg, writer)


if __name__ == '__main__':
    args = get_args()
    config = get_config(args)

    train(config)
