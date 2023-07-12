# Wheather Report
Python script  that fetches data from _Oanda_ or _Finnhub_ API, saves 
**Ichimoku Cloud** and **Commodity Channel Index** plots and in other file 
**MACD** and **RSI** for Daily and 1 hour timeperiod - useful for real trading,
unless you are looking for daytrading help, then that's not what you're looking
for. Intended for patient and well versed traders tired of looking at charts 
from their platform. Simplified view of microeconomics to midsized trends that
occur on Forex and Stock market. Are you ready to take a leap of faith and pursue
the dangerous path of not starring day and night at your _crypto_ wallet?

## Examples

### 1 Hour timeframe
![CHF/JPY 1 Hour chart](CHF_JPY%20-%201%20Hour%20-%202023-03-08-T16_00_00Z.png "CHF/JPY 1 Hour")

![CHF/JPY 1 Hour MACD and RSI plot](CHF_JPY%20-%201%20Hour%20MACD%20and%20RSI%20-%202023-05-23-T09_00_00Z.png "CHF/JPY 1 Hour MACD and RSI")

### Daily timeframe
![CHF/JPY Daily chart](CHF_JPY%20-%20Day%20-%202023-03-07-T22_00_00Z.png "CHF/JPY Daily")

![CHF/JPY Daily MACD and RSI plot](CHF_JPY%20-%20Day%20MACD%20and%20RSI%20-%202023-05-22-T21_00_00Z.png "CHF/JPY Daily MACD and RSI")

## Usage

You will need Python 3 (__3.10!__ _MAX_) and libraries included in `requirements.txt` file

```shell
# for virtualenv
pip install -r requirements.txt
# for python3
python3 -m pip install -r requirements.txt
```

Invoke above command to install required modules.

Then you can get simple help using this command:

```python
python3 wheater_report.py --help
```

This should output:

```bash
usage: wheather_report.py [-h] --token TOKEN [--account ACCOUNT] [--practice] [--instruments INSTRUMENTS] [--list]
                          [--stocks]

Wheather Report v0.1
This program should help you get the most out of the market.
Just let the money flow, and don't swim with the sharks!.
Author: Szymon Błaszczyński for Nutek Security Solutions

::::    ::: :::    ::: ::::::::::: :::::::::: :::    :::
:+:+:   :+: :+:    :+:     :+:     :+:        :+:   :+:
:+:+:+  +:+ +:+    +:+     +:+     +:+        +:+  +:+
+#+ +:+ +#+ +#+    +:+     +#+     +#++:++#   +#++:++
+#+  +#+#+# +#+    +#+     +#+     +#+        +#+  +#+
#+#   #+#+# #+#    #+#     #+#     #+#        #+#   #+#
###    ####  ########      ###     ########## ###    ###


Example usage:
python3 weather_report.py --token <your_oanda_token> --account <your_account_id> --instruments EUR_USD,USD_JPY,GBP_USD
python3 weather_report.py --token <your_oanda_token> --account <your_account_id> --instruments all
python3 weather_report.py --token <your_oanda_oken> --account <your_account_id> --list
python3 weather_report.py --token <your_oanda_demo_token> --account <your_account_id> --practice --instruments EUR_USD,USD_JPY,GBP_USD
python3 weather_report.py --token <your_finnhub_token> --stocks --instruments AAPL,MSFT,AMZN
python3 weather_report.py --token <your_finnhub_token> --stocks --list | less

options:
  -h, --help            show this help message and exit
  --token TOKEN         Enter your Oanda API token
  --account ACCOUNT     Enter your account id (required for Oanda)
  --practice            Wheter to use Oanda practice account
  --instruments INSTRUMENTS
                        Enter the instruments to download plots or all
  --list                List all instruments
  --stocks              Wheter to use stocks data (provide Finnhub API key as --token)
```

- **token** - your Oanda/Finnhub API token - visit [getting starded on oanda.com](https://developer.oanda.com/rest-live-v20/introduction/) for more
  information about how to get this token (you can get one for a demo account)
  or [register on Finnhub](https://finnhub.io/register) - this argument is required
- **account** - you have to provide an account id from which the data will be fetched - this argument is required for Oanda requests
- **practice** - if you give this command, this program will change the source of information to demo aka practice account - this argument is optional and
intended for use with Oanda type of requests, if you prefer to use DEMO account.
- **stock** - insist you want to have an information about some stock/s
- **instruments** - choose what you want to get, one or more (separeted by coma or space), even all (_not_ recommended)
- **list** - get list of US stocks available to show (--stock), or Oanda instruments.

## License

MIT - do what you want, but don't forget to include the license file if you're sharing. Also, pet the cat and fly safe!
