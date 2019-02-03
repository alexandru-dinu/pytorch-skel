# PyTorch skel

Experiment-based skeleton for ML/DL projects in PyTorch.
**Expect updates (e.g. after testing with CV, NLP models).**

### Usage

- Each experiment configuration must be defined as a new json in `./configs`
- Models and model-related code must be placed under `./models`
- Training will create the needed dirs for this experiment 
(i.e. `./experiments/<name>/out/` and `./experiments/<name>/chkpt/`)
- Testing will load a specific checkpoint and data

### Goals

- Project agnostic lift-off for PyTorch
- Easier way of managing experiments
- Consistent reporting
