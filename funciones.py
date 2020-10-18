# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:44:51 2020

@author: tomvc
"""

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from sodapy import Socrata
import holidays
import warnings
warnings.filterwarnings('ignore')

def get_TRM(fecha):
    client = Socrata("www.datos.gov.co", None)
    w = "vigenciadesde >= '{}'".format(dt.datetime.strftime(dt.date(2008, 1, 1), '%Y-%m-%d'))
    r = client.get("32sa-8pi3", where=w, limit=10000000)
    df = pd.DataFrame.from_records(r)
    df = df[['vigenciadesde', 'valor']]
    df.columns = ['Fecha', 'TRM']
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df = df[df.Fecha <= fecha]
    df['Fecha'] = [i - dt.timedelta(days=1) for i in df['Fecha']]
    df['TRM'] = pd.to_numeric(df['TRM'])
    df.sort_values('Fecha', inplace=True)
    return df

def get_data(ticker, fecha_inicial, fecha_final):
    df = yf.download(ticker, 
                       start=dt.datetime.strftime(fecha_inicial, '%Y-%m-%d'),
                       end=dt.datetime.strftime(fecha_final, '%Y-%m-%d'),
                       progress=False)
    df.reset_index(level=0, inplace=True)
    return df

def ultDiaHabil():
    f = dt.date.today() - dt.timedelta(days=1)
    while True:
        if f in holidays.CO() or f.weekday() == 5 or f.weekday() == 6:
            f = f - dt.timedelta(days=1)
        else:
            break
    return f

def get_TRM_BoxPlot(fecha):
    df = get_TRM(fecha)
    df['MA'] = pd.to_datetime(df['Fecha']).dt.to_period('M')
    df = df[df.Fecha > dt.datetime(2009, 12, 31, 0, 0, 0)]
    return df

def trm_table_yr(fecha):
    df = get_TRM(fecha)
    df.set_index('Fecha', inplace=True)
    df = df.groupby(pd.Grouper(freq='Y')).agg(
            {'TRM' : ['min', 'max', 'mean', np.std]}
            ).dropna()
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '${:0,.2f}'.format(x))
    df.reset_index(level=0, inplace=True)
    df['Fecha'] = [i.year for i in df['Fecha']]
    df.columns=['Fecha', 'Mínimo', 'Máximo', 'Media', 'Std_Dev']
    return df

dict_ind = {'SMA(14)' : 14, 'SMA(50)' : 50, 'SMA(200)' : 200, 'BB' : 0}

def boll_bands(df):
    df['TP'] = (df['Close'] + df['High'] + df['Low']) / 3
    df['Std'] = df['TP'].rolling(20).std()
    df['BB+'] = df['TP'].rolling(20).mean() + (df['Std'] * 2)
    df['BB-'] = df['TP'].rolling(20).mean() - (df['Std'] * 2)
    return list(df['BB+']), list(df['BB-'])

def macd(df):
    df['ema12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['ema26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    return list(df['macd']), list(df['signal'])

def RSI(df):
    df['R'] = np.log(df['Close'] / df['Close'].shift(1))
    R = list(df['R'])
    rsi = [np.nan] * 14
    for i in range(14, len(R)):
        r = R[i-14:i]
        pos = []
        neg = []
        for j in r:
            if j < 0:
                neg.append(j)
            elif j > 0:
                pos.append(j)
            else:
                pos.append(0)
                neg.append(0)
        rs = (sum(pos) / len(pos)) / abs((sum(neg) / len(neg)))
        rsi.append(100 - (100 / (1 + rs)))
    return rsi

def SO(df):
    df['H'] = df['Close'].rolling(14).max()
    df['L'] = df['Close'].rolling(14).min()
    df['SO'] = ((df['Close'] - df['L']) / (df['H'] - df['L'])) * 100
    df['SOM'] = df['SO'].rolling(3).mean()
    return list(df['SO']), list(df['SOM'])

def df_stocks(nemo, fecha, fecha_inicial, ind1, ind2):
    fecha_inicial = fecha_inicial - dt.timedelta(days=2000)
    df = get_data(nemo, fecha_inicial, fecha)
    if len(ind1) > 0:
        for col in ind1:
            if col != 'BB':
                df[col] = df['Close'].rolling(dict_ind[col]).mean()
            else:
                bbu, bbd = boll_bands(df.loc[:, ['Date', 'Close', 'High', 'Low']])
                df['BB+'] = bbu
                df['BB-'] = bbd
                
    if ind2 == 'MACD':
        m, s = macd(df.loc[:, ['Close']])
        df['MACD'] = m
        df['MACD_Signal'] = s
    elif ind2 == 'RSI':
        df['RSI'] = RSI(df)
    elif ind2 == 'Stochastic Oscillator':
        so, som = SO(df.loc[:, ['Close']])
        df['Stochastic Oscillator'] = so
        df['SO_SMA'] = som
    
    return df