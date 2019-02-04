import os
import sys
from argparse import Namespace

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import logger
from utils import get_config, get_args, dump_cfg

# models
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../models"))

from mnist_model import Net


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
    logger.info("=== Testing ===")

    # initial setup
    prologue(cfg)

    model = Net()
    model.eval()
    model.load_state_dict(torch.load(cfg.chkpt))
    if cfg.device == "cuda":
        model.cuda()

    logger.info("Loaded model")

    dataloader = torch.utils.data.DataLoader(
        datasets.MNIST('../mnist-data', train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=1, shuffle=cfg.shuffle, num_workers=cfg.num_workers
    )

    logger.info("Loaded data")

    loss_criterion = nn.NLLLoss()

    correct, test_loss = 0.0, 0.0

    for batch_idx, data in enumerate(dataloader, start=1):
        img, target = data

        if cfg.device == "cuda":
            img, target = img.cuda(), target.cuda()

        out = model(img)
        test_loss += loss_criterion(out, target).item()

        pred = out.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum().item()

        if batch_idx % cfg.batch_every == 0:
            logger.debug("[%5d/%5d] run_loss: %.8f" % (batch_idx, len(dataloader), test_loss / batch_idx))

    logger.info('Test set: Average loss: %.8f, Accuracy: %.8f\n' % (test_loss / len(dataloader), correct / len(dataloader)))

    # final setup
    epilogue(cfg)


if __name__ == '__main__':
    args = get_args()
    config = get_config(args)

    test(config)
