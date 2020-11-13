# bagoftools

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/alexandru-dinu/bagoftools/blob/master/LICENSE)
[![pypi](https://img.shields.io/pypi/v/bagoftools.svg)](https://pypi.org/project/bagoftools/)

## Install

```bash
pip install bagoftools
```

## Contents

```yaml
- namespace:
  - Namespace     # Recursive namespace (useful for managing experiment configurations).
- logger:
  - Logger        # Wrapper over Python's logger, colorized and more user-friendly.
- plotting:
  - stem_hist     # Histogram on a stem plot.
- processing:
  - map_batchwise # Map a function over a batch of data and collect the results.
  - get_batches   # Split the input array in batches of given size.
```

## Disclaimer

The sole purpose of this package is to speed-up prototyping. It is not recommended to be used in production environments.
