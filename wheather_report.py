import pandas as pd
import numpy as np
import requests
from datetime import datetime
import mplfinance as mpf
import matplotlib.pyplot as plt
import talib
import os
import argparse
from argparse import RawTextHelpFormatter
from progress1bar import ProgressBar
import finnhub
import csv

def plotting(frame,title,path):
    
    mc = mpf.make_marketcolors(up='g',down='r',alpha=0.5,volume={'up':'g','down':'r'})
    s  = mpf.make_mpf_style(base_mpf_style='yahoo',marketcolors=mc,gridstyle='')
    
    fig = mpf.figure(style=s,figsize=(16,9))
    ax1 = fig.add_subplot(3,1,1)
    last_date = frame.index[-1]
    title_of_plot = "{} Ichiomku and CCI - {}".format(title, str(last_date.strftime('%Y-%m-%d-T%H_%M_%SZ')))
    ax1.set_title(title_of_plot)
    ax2 = fig.add_subplot(3,1,2,sharex=ax1)
    ax3 = fig.add_subplot(3,1,3,sharex=ax1)
    high9=frame.High.rolling(9).max()
    Low9=frame.High.rolling(9).min()
    high26=frame.High.rolling(26).max()
    Low26=frame.High.rolling(26).min()
    high52=frame.High.rolling(52).max()
    Low52=frame.High.rolling(52).min()

    frame['tenkan_sen']=(high9+Low9)/2
    frame['kijun_sen']=(high26+Low26)/2
    frame['chikou']=frame.Close.shift(-26)
    frame=frame.shift(-26)
    frame['senkou_A']=((frame.tenkan_sen+frame.kijun_sen)/2).shift(26)
    frame['senkou_B']=((high52+Low52)/2).shift(26)

    cci = talib.CCI(frame['High'], frame['Low'], frame['Close'], timeperiod=20)
    frame['cci'] = cci

    frame['cci_overbought'] = [100.]*len(frame)
    frame['cci_oversold'] = [-100.]*len(frame)
    apds = [mpf.make_addplot(frame['cci'],ax=ax3,color='g',ylabel='CCI',mav=(20)),
            mpf.make_addplot(frame[ ['cci_overbought','cci_oversold'] ], ax=ax3, linestyle='-.',secondary_y=False),
            mpf.make_addplot(frame['tenkan_sen'],ax=ax1),
            mpf.make_addplot(frame['kijun_sen'],ax=ax1),
            mpf.make_addplot(frame['chikou'],ax=ax1),
            mpf.make_addplot(frame.senkou_A,ax=ax1,color='magenta',alpha=0.5),
            mpf.make_addplot(frame.senkou_B,ax=ax1,color='red',alpha=0.5)]

    ax1.fill_between([x for x in range(0,len(frame))],frame.senkou_A,frame.senkou_B,where=frame.senkou_A>=frame.senkou_B,color='lightgreen')
    ax1.fill_between([x for x in range(0,len(frame))],frame.senkou_A,frame.senkou_B,where=frame.senkou_A<frame.senkou_B,color='lightcoral')
    ax3.fill_between([x for x in range(0,len(frame))],frame.cci,frame.cci_overbought,where=frame.cci>frame.cci_overbought,color='lightcoral')
    ax3.fill_between([x for x in range(0,len(frame))],frame.cci,frame.cci_oversold,where=frame.cci<frame.cci_oversold,color='lightgreen')
    mpf.plot(frame,ax=ax1,volume=ax2,type='line',xrotation=0,addplot=apds,tight_layout=True)
    fig.savefig("{}/{}.png".format(path, title_of_plot))
    plt.close(fig)
    
    # MACD and RSI chart
    fig = mpf.figure(style=s,figsize=(16,9))
    ax1 = fig.add_subplot(4,1,1)
    ax2 = fig.add_subplot(4,1,2,sharex=ax1)
    ax3 = fig.add_subplot(4,1,3,sharex=ax1)
    ax4 = fig.add_subplot(4,1,4,sharex=ax1)
    last_date = frame.index[-1]
    title_of_plot = "{} MACD and RSI - {}".format(title, str(last_date.strftime('%Y-%m-%d-T%H_%M_%SZ')))
    ax1.set_title(title_of_plot)
    # Calculate the MACD
    exp12     = frame['Close'].ewm(span=12, adjust=False).mean()
    exp26     = frame['Close'].ewm(span=26, adjust=False).mean()
    macd      = exp12 - exp26
    signal    = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    fb_green = dict(y1=macd.values,y2=signal.values,where=signal<macd,color="#93c47d",alpha=0.6,interpolate=True)
    fb_red   = dict(y1=macd.values,y2=signal.values,where=signal>macd,color="#e06666",alpha=0.6,interpolate=True)
    fb_green['panel'] = 1
    fb_red['panel'] = 1
    fb       = [fb_green,fb_red]
    # Calculate the RSI
    rsi = talib.RSI(frame["Close"], timeperiod=14)
    frame['rsi'] = rsi
    frame['rsi_overbought'] = [70.]*len(frame)
    frame['rsi_oversold'] = [30.]*len(frame)
    apds = [#mpf.make_addplot(exp12,color='lime'),
            #mpf.make_addplot(exp26,color='c'),
            mpf.make_addplot(histogram,type='bar',width=0.7,
                            color='dimgray',alpha=1,secondary_y=True,ax=ax2),
            mpf.make_addplot(macd,
                             ylabel='MACD',
                             color='fuchsia',secondary_y=False,ax=ax2),
            mpf.make_addplot(signal,
                             color='b',secondary_y=False,ax=ax2),
            mpf.make_addplot(rsi, 
                            ylabel='RSI',
                               ax=ax3),
            mpf.make_addplot(frame['rsi_overbought'], 
                               linestyle='-.',secondary_y=False, color='red',ax=ax3),
            mpf.make_addplot(frame['rsi_oversold'], 
                               linestyle='-.',secondary_y=False, color='green',ax=ax3),
        ]
    ax3.fill_between([x for x in range(0,len(frame))],frame.rsi,frame.rsi_overbought,where=frame.rsi>frame.rsi_overbought,color='lightcoral')
    ax3.fill_between([x for x in range(0,len(frame))],frame.rsi,frame.rsi_oversold,where=frame.rsi<frame.rsi_oversold,color='lightgreen')
    # Plot the data
    mpf.plot(frame,
             ax=ax1,
             volume=ax4,
             type='line',xrotation=0,addplot=apds,tight_layout=True,
             fill_between=fb)
    fig.savefig("{}/{}.png".format(path, title_of_plot))
    plt.close(fig)


def parse_ohlc(response):
    # Extract candle data from response
    data = response.json()['candles']
    df = pd.DataFrame(data)
    df = df[['time', 'bid', 'volume']]

    # Convert time to datetime and set as index
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # Convert mid prices to float
    ohlc = df['bid'].apply(pd.Series).astype(float)

    ohlc['volume'] = df['volume']

    # Rename columns
    ohlc.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return ohlc

def parse_finnohlc(response):
    # Extract candle data from response
    df = pd.DataFrame(response)
    # convert to datetime
    df['time'] = pd.to_datetime(df['t'], unit='s')
    # set index
    df.set_index('time', inplace=True)

    # Convert mid prices to float
    ohlc = df[['c', 'h', 'l', 'o']].apply(pd.Series).astype(float)

    ohlc['volume'] = df['v']

    # Rename columns
    ohlc.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    return ohlc

program_description = '''Wheather Report v0.1
This program should help you get the most out of the market.
Just let the money flow, and don't swim with the sharks!.
Author: Szymon Błaszczyński for Nutek Security Solutions

\033[1;31m::::    ::: :::    ::: ::::::::::: :::::::::: :::    :::
\033[1;31m:+:+:   :+: :+:    :+:     :+:     :+:        :+:   :+:
\033[1;32m:+:+:+  +:+ +:+    +:+     +:+     +:+        +:+  +:+
\033[1;32m+#+ +:+ +#+ +#+    +:+     +#+     +#++:++#   +#++:++
\033[1;32m+#+  +#+#+# +#+    +#+     +#+     +#+        +#+  +#+
\033[1;34m#+#   #+#+# #+#    #+#     #+#     #+#        #+#   #+#
\033[1;34m###    ####  ########      ###     ########## ###    ###
\033[0m

Example usage:
python3 weather_report.py --token <your_oanda_token> --account <your_account_id> --instruments EUR_USD,USD_JPY,GBP_USD
python3 weather_report.py --token <your_oanda_token> --account <your_account_id> --instruments all
python3 weather_report.py --token <your_oanda_oken> --account <your_account_id> --list
python3 weather_report.py --token <your_oanda_demo_token> --account <your_account_id> --practice --instruments EUR_USD,USD_JPY,GBP_USD
python3 weather_report.py --token <your_finnhub_token> --stocks AAPL,MSFT,AMZN
python3 weather_report.py --token <your_finnhub_token> --list-exchanges 
python3 weather_report.py --token <your_finnhub_token> --exchange WA | less

'''
# Create an ArgumentParser object
parser = argparse.ArgumentParser(description=program_description, formatter_class=RawTextHelpFormatter)
# Add a named argument
parser.add_argument('--token', type=str, help='Enter your Oanda API token', required=True)
parser.add_argument('--account', type=str, help='Enter your account id (required for Oanda)', required=False)
parser.add_argument('--practice', action='store_true', help='Wheter to use Oanda practice account')
parser.add_argument('--instruments', type=str, help='Enter the Oanda instruments to download plots or all', required=False)
parser.add_argument('--list', action='store_true', help='List all Oanda (CFD) instruments')
parser.add_argument('--stocks', type=str, help='Enter stock tickers to download plots (provide Finnhub API key as --token) using all require --exchange to download from', required=False)
parser.add_argument('--list-exchanges', action='store_true', help='List all stock exchanges')
parser.add_argument('--exchange', type=str, help='List stocks on exchange [default: US]', required=False)
# Parse the command-line arguments
args = parser.parse_args()

if args.exchange:
    finnhub_client = finnhub.Client(api_key=args.token)
    instruments = finnhub_client.stock_symbols(args.exchange)
    # get only symbols
    instruments = [x['symbol'] for x in instruments]
    # sort alphabetically
    instruments.sort()
    for instrument in instruments:
        print(instrument)
    exit()
if args.list_exchanges:
    finnhub_client = finnhub.Client(api_key=args.token)
    # https://finnhub.io/docs/api/stock-symbols
    # Read csv file Finnhub Exchanges.csv from the same directory
    file = open('Finnhub Exchanges.csv', 'r')
    exchanges = csv.reader(file)
    exchanges = list(exchanges)
    # print all exchanges
    for exchange in exchanges[1:]:
        print('{} - {}'.format(exchange[0], exchange[1]))
    file.close()
    exit()
if args.stocks:
    finnhub_client = finnhub.Client(api_key=args.token)
    # time now in milliseconds
    now = datetime.now()
    # convert to seconds
    now = now.timestamp()
    # 1250 hours ago
    then_h = now - 1250 * 60 * 60
    # 1250 days ago
    then_d = now - 1250 * 24 * 60 * 60
    # Format datetime as string
    now_utc = datetime.utcnow()
    formatted_date = now_utc.strftime('%Y-%m-%d-T%H_%M_%SZ')
    # specify the directory path
    directory_path = "finance_charts-{}".format(formatted_date)
    # check if directory exists, if not then create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created at {directory_path}")
    else:
        print(f"Directory already exists at {directory_path}")
    instruments = []
    if args.stocks == 'all':
        # get all instruments
        instruments = finnhub_client.stock_symbols(args.exchange)
        # get only symbols
        instruments = [x['symbol'] for x in instruments]
    else:
        instruments = args.stocks.split(',')
        if len(instruments) < 1:
            instruments = args.stocks.split(' ')
            if len(instruments) < 1:
                instruments = args.stocks
                if len(instruments) < 1:
                    print('No instruments provided')
                    exit(1)
    print("Downloading {} instruments".format(len(instruments)))
    completed_message = 'Download and chart drawing complete'
    with ProgressBar(total=len(instruments), completed_message=completed_message, clear_alias=True, show_fraction=False, show_prefix=False, show_duration=True) as pb:
        for instrument in instruments:
            pb.alias = instrument
            # Stock candles
            res_d = finnhub_client.stock_candles(instrument, 'D', int(then_d), int(now))
            res_h1 = finnhub_client.stock_candles(instrument, '60', int(then_h), int(now))
            # save to csv
            # df.to_csv('{}.csv'.format(instrument))
            # plot
            ohlc_d = parse_finnohlc(res_d)
            ohlc_h1 = parse_finnohlc(res_h1)
            plotting(ohlc_d,  "{} - {}".format(instrument, "Day"), directory_path)
            plotting(ohlc_h1,  "{} - {}".format(instrument, "1 Hour"), directory_path)
            pb.count += 1
    exit()

if args.practice:
    uri = 'https://api-fxpractice.oanda.com/v3/'
else:
    uri = 'https://api-fxtrade.oanda.com/v3/'
# Set up the API endpoint URL and request headers
endpoint = '{}accounts/{}/instruments/'.format(uri, args.account)
headers = {'Authorization': 'Bearer {}'.format(args.token),
           'Content-Type': 'application/json'}
response = requests.get(endpoint, headers=headers)
instruments = response.json()['instruments']
if args.list:
    # sort alphabetically
    instruments.sort(key=lambda x: x['name'])
    for instrument in instruments:
        print(instrument['name'])
    exit()
now = datetime.utcnow()
# Get current datetime
# Format datetime as string
formatted_date = now.strftime('%Y-%m-%d-T%H_%M_%SZ')
# specify the directory path
directory_path = "finance_charts-{}".format(formatted_date)
# check if directory exists, if not then create it
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"Directory created at {directory_path}")
else:
    print(f"Directory already exists at {directory_path}")
inst_len = len(instruments)
if args.instruments == 'all':
    pass
else:
    instruments_args = args.instruments.split(',')
    if len(instruments_args) == 0:
        instruments_args = args.instruments.split(' ')
        if len(instruments_args) == 0:
            print("Instrument {} not found".format(args.instruments))
            exit()
    instruments = [x for x in instruments if x['name'] in instruments_args]
    if len(instruments) == 0:
        print("Instrument {} not found".format(args.instruments))
        exit()
print("Downloading {} instruments".format(len(instruments)))
completed_message = 'Download and chart drawing complete'
with ProgressBar(total=len(instruments), completed_message=completed_message, clear_alias=True, show_fraction=False, show_prefix=False, show_duration=True) as pb:
    for index, instrument in enumerate(instruments):
        pb.alias = instrument['name']
        instrument_name = instrument['name']
        # Set up the API endpoint URL and request headers
        endpoint = '{}instruments/{}/candles'.format(uri, instrument_name)
        headers = {'Authorization': 'Bearer {}'.format(args.token),
            'Content-Type': 'application/json'}
        # Set up the request parameters
        params = {'price': 'B',
            'count': 1250,
            'granularity': 'H1'}
        response_h1 = requests.get(endpoint, headers=headers, params=params)
        params = {'price': 'B',
            'count': 1250,
            'granularity': 'D'}
        response_d = requests.get(endpoint, headers=headers, params=params)
        ohlc_h1 = parse_ohlc(response_h1)
        ohlc_d = parse_ohlc(response_d)   
        plotting(ohlc_h1, "{} - {}".format(instrument_name, "1 Hour"), directory_path)
        plotting(ohlc_d,  "{} - {}".format(instrument_name, "Day"), directory_path)
        pb.count += 1