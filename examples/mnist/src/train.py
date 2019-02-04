import os
import sys
from argparse import Namespace

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import logger
from utils import get_config, get_args, dump_cfg

# models
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../models"))

from mnist_model import Net


def prologue(cfg: Namespace, *varargs) -> None:
    # sanity checks
    assert cfg.device == "cpu" or (cfg.device == "cuda" and torch.cuda.is_available())

    # dirs
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

    model = Net()
    model.train()
    if cfg.device == "cuda":
        model.cuda()

    logger.debug("Model loaded")


    dataloader = torch.utils.data.DataLoader(
        datasets.MNIST('../mnist-data', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=cfg.batch_size, shuffle=cfg.shuffle, num_workers=cfg.num_workers
    )

    logger.debug("Data loaded")

    optimizer = optim.Adam(model.parameters(), lr=cfg.learning_rate)
    loss_criterion = nn.NLLLoss()
    avg_loss, epoch_avg = 0.0, 0.0

    # train-loop
    for epoch_idx in range(cfg.start_epoch, cfg.num_epochs + 1):

        for batch_idx, data in enumerate(dataloader, start=1):
            img, target = data
            if cfg.device == "cuda":
                img, target = img.cuda(), target.cuda()

            img, target = Variable(img), Variable(target)

            optimizer.zero_grad()

            out = model(img)

            loss = loss_criterion(out, target)

            avg_loss += loss.item()
            epoch_avg += loss.item()

            loss.backward()

            optimizer.step()

            if batch_idx % cfg.batch_every == 0:
                logger.debug(
                    '[%3d/%3d][%5d/%5d] avg_loss: %.8f' %
                    (epoch_idx, cfg.num_epochs, batch_idx, len(dataloader), avg_loss / cfg.batch_every)
                )
                avg_loss = 0.0
        # -- batch-loop

        if epoch_idx % cfg.epoch_every == 0:
            logger.info("Epoch avg = %.8f" % (epoch_avg / (len(dataloader) * cfg.epoch_every)))
            epoch_avg = 0.0
            torch.save(model.state_dict(), f"../experiments/{cfg.exp_name}/chkpt/model_{epoch_idx}.pth")
    # -- train-loop

    # save final model
    torch.save(model.state_dict(), f"../experiments/{cfg.exp_name}/model_final.pth")

    # final setup
    epilogue(cfg)


if __name__ == '__main__':
    args = get_args()
    config = get_config(args)

    train(config)
