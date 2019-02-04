# PyTorch skel

Experiment-based skeleton for ML/DL projects in PyTorch.
**Expect updates (e.g. after testing with CV, NLP models).**


### Goals

- Project agnostic lift-off for PyTorch
- Easier way of managing experiments
- Consistent reporting


### Usage

- Each experiment configuration must be defined as a new json in `./configs`
- Models and model-related code must be placed under `./models`
- Training will create the needed dirs for this experiment
(i.e. `./experiments/<name>/out/` and `./experiments/<name>/chkpt/`)
- Testing will load a specific checkpoint and data
- `prologue` and `epilogue` functions in `train.py` and `test.py` are generic
functions which deal with setting / cleaning up the training / testing
- There is a TensorBoard writer for training reporting which currently shows the
computational graph, the average loss per batch-interval, and histograms for model's parameters
