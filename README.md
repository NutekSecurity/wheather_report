# Ichimoku-CCI_H1-D
Python script  that fetches data from Oanda API, saves Ichimoku Cloud and Commodity Channel Index plots

## Examples

### 1 Hour timeframe
![CHF/JPY 1 Hour chart](CHF_JPY%20-%201%20Hour%20-%202023-03-08-T16_00_00Z.png "CHF/JPY 1 Hour")

### Daily timeframe
![CHF/JPY Daily chart](CHF_JPY%20-%20Day%20-%202023-03-07-T22_00_00Z.png "CHF/JPY Daily")

## Usage

You will need Python 3 and this libraries (some are included in certain Python distributions - I have used `Anaconda Python`)

```python
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import mplfinance as mpf
import matplotlib.pyplot as plt
import talib
import os
import sys
import argparse
```

Then you can get simple help using this command:

```python
python3 ichi_cci_h1_d.py --help
```

This should output:

```bash
usage: ichi_cci_h1_d.py [-h] --token TOKEN --account ACCOUNT [--practice]

optional arguments:
  -h, --help         show this help message and exit
  --token TOKEN      Enter your Oanda API token
  --account ACCOUNT  Enter your account id
  --practice         Wheter to use Oanda practice account
```

- **token** - your Oanda API token - visit [getting starded on oanda.com](https://developer.oanda.com/rest-live-v20/introduction/) for more
  information about how to get this token (you can get one for a demo account) - this argument is required
- **account** - you have to provide an account id from which the data will be fetched - this argument is required
- **practice** - if you give this command, this program will change the source of information to demo aka practice account - this argument is optional

When you run the program like this:

```bash
python3 ichi_cci_h1_d.py --token xxx-xxx --account xxx-xxx
```

it will download the data from Oanda.com and save the charts/plots to the folder relative to it's invocation path and you will have beatiful Ichimoku
Cloud with Volume, Commodity Channel Index and price in one place for future reference.

## License

MIT - do what you want, but don't forget to include the license file if you're sharing. Also, pet the cat and fly safe!
