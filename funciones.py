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
            f = dt.timedelta(days=1)
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
