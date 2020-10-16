# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:44:51 2020

@author: tomvc
"""

import pandas as pd
import yfinance as yf
import datetime as dt
from sodapy import Socrata
import holidays

def get_TRM():
    client = Socrata("www.datos.gov.co", None)
    w = "vigenciadesde >= '{}'".format(dt.datetime.strftime(dt.date(2008, 1, 1), '%Y-%m-%d'))
    r = client.get("32sa-8pi3", where=w, limit=10000000)
    df = pd.DataFrame.from_records(r)
    df = df[['vigenciadesde', 'valor']]
    df.columns = ['Fecha', 'TRM']
    df['Fecha'] = pd.to_datetime(df['Fecha'])
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
    return df[['Date', 'Close', 'Open', 'High', 'Low']]

def ultDiaHabil():
    f = dt.date.today() - dt.timedelta(days=1)
    while True:
        if f in holidays.CO() or f.weekday() == 5 or f.weekday() == 6:
            f = dt.timedelta(days=1)
        else:
            break
    return f

f = ultDiaHabil()