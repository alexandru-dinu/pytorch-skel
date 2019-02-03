import argparse
import json


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--cfg", type=str, required=True)

    return parser.parse_args()


def get_config(args: argparse.Namespace) -> argparse.Namespace:
    cfg_dict = json.load(open(args.cfg, "rt"))
    return argparse.Namespace(**cfg_dict)


def dump_cfg(file: str, cfg: dict) -> None:
    fp = open(file, "wt")
    for k, v in cfg.items():
        fp.write("%15s: %s\n" % (k, v))
    fp.close()
