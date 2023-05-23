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

# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add a named argument
parser.add_argument('--token', type=str, help='Enter your Oanda API token', required=True)
parser.add_argument('--account', type=str, help='Enter your account id', required=True)
parser.add_argument('--practice', action='store_true', help='Wheter to use Oanda practice account')
# Parse the command-line arguments
args = parser.parse_args()
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
now = datetime.utcnow()
# Get current datetime
# Format datetime as string
formatted_date = now.strftime('%Y-%m-%d-T%H_%M_%SZ')
# specify the directory path
directory_path = "oanda_charts-{}".format(formatted_date)
# check if directory exists, if not then create it
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"Directory created at {directory_path}")
else:
    print(f"Directory already exists at {directory_path}")
inst_len = len(instruments)
print("Progress: ", end='')
for index, instrument in enumerate(instruments):
    progress = index / inst_len * 100
    if index == 0:
        print("0.5%... ".format(progress), end='')
    elif index % 5 == 0:
        print("{}%... ".format(progress), end='')
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
    exit()