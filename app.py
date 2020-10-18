# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 20:04:12 2020

@author: tomvc
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import datetime as dt
import pandas as pd
import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
suppress_callback_exceptions = True

from funciones import ultDiaHabil, get_TRM, get_data, get_TRM_BoxPlot, trm_table_yr, df_stocks

#Cartas y Tab 1 ---> TRM vs Petroleo-------------------------------------------

trm_oil_1 = dbc.Card([
                dcc.Graph(id='graf')
                ])

trm_box = dbc.Card([
        dcc.Graph(id='trm-box')
        ])

corr = dbc.Card([
        dbc.CardBody([
                html.H4('Correlación TRM vs Petróleo'),
                html.H6('Fecha desde: '),
                dcc.DatePickerSingle(id='date-corr',
                                    date=ultDiaHabil() - dt.timedelta(days=365),
                                    min_date_allowed=dt.date(2009, 1, 1),
                                    max_date_allowed=ultDiaHabil(),
                                    display_format = 'D/M/Y',
                                    persistence=False),
                dcc.Graph(id='corr')
                ])
        ])

trm_table = dbc.Card([
        dbc.CardBody([
                html.H4('Información TRM Anual'),
                dash_table.DataTable(id='trm-table',
                                     merge_duplicate_headers=True,
                                     style_table={'overflowX' : 'auto'},
                                     style_data_conditional=[
                                             {'if' : {'row_index' : 'odd'},
                                              'backgroundColor' : 'rgb(248, 248, 248)'}],
                                     style_header={'backgroundColor' : 'rgb(230, 230, 230)',
                                                   'fontWeight' : 'bold'},
                                     style_cell={'textAlign' : 'center'}
                                             )
                ])
        ])

trm_oil = html.Div([
        dbc.Row(dbc.Col(html.Div(html.Br()))),
        dbc.Row([
                dbc.Col(html.H4('Fecha de Corte: '), width={'size' : 'auto', 'offset' : 1}),
                dbc.Col(dcc.DatePickerSingle(id='fecha_corte',
                                             date = ultDiaHabil(),
                                             min_date_allowed = dt.date(2009, 1, 1),
                                             max_date_allowed = ultDiaHabil(),
                                             display_format = 'D/M/Y',
                                             persistence=False), width='auto'),
                dbc.Col(html.H4('Frecuencia: '), width='auto'),
                dbc.Col(dbc.RadioItems(id='freq',
                                       value='Diaria',
                                       options=[{'label' : 'Diaria ', 'value' : 'Diaria'},
                                                {'label' : 'Mensual ', 'value' : 'Mensual'},
                                                {'label' : 'Anual ', 'value' : 'Anual'}],
                                                inline=True), width=4)
                ], justify='start'),
        dbc.Row(dbc.Col(html.Div(html.Br()))),
        dbc.Row([
                dbc.Col(trm_oil_1, width={'size' : 10, 'offset' : 1}),
                ]),
        dbc.Row(dbc.Col(html.Div(html.Br()))),
        dbc.Row([
                dbc.Col(trm_box, width={'size' : 10, 'offset' : 1}),
                ]),
        dbc.Row(dbc.Col(html.Div(html.Br()))),
        dbc.Row([
                dbc.Col(corr, width={'size' : 5, 'offset' : 1}),
                dbc.Col(trm_table, width=5)
                ]),
        ])
#------------------------------------------------------------------------------

#Cartas y Tab 2 ---> Acciones S&P----------------------------------------------
dict_acc = {'S&P' : '^GSPC', 'Apple' : 'AAPL', 'Microsoft' : 'MSFT',
            'Amazon' : 'AMZN', 'Facebook' : 'FB', 'Alphabet' : 'GOOG',
            'Berkshire Hathaway' : 'BRK-B', 'Johnson & Johnson' : 'JNJ',
            'VISA' : 'V', 'Procter & Gamble' : 'PG'}

ind_1 = dbc.Card([
        dbc.CardBody([
            dbc.Label('Panel Principal: '),
            dbc.Checklist(
                    value=['SMA(14)'],
                    options=[
                                {'label' : 'SMA(14)', 'value' : 'SMA(14)'},
                                {'label' : 'SMA(50)', 'value' : 'SMA(50)'},
                                {'label' : 'SMA(200)', 'value' : 'SMA(200)'},
                                {'label' : 'Bollinger Bands', 'value' : 'BB'},
                            ],
                    id='ind-1',
                    inline=True
                )
            ])
        ])

ind_2 = dbc.Card([
        dbc.CardBody([
            dbc.Label('Panel Secundario: '),
            dbc.RadioItems(
                    value='MACD',
                    options=[
                                {'label' : 'RSI', 'value' : 'RSI'},
                                {'label' : 'MACD', 'value' : 'MACD'},
                                {'label' : 'Stochastic Oscillator', 'value' : 'Stochastic Oscillator'}                                
                            ],
                    id='ind-2',
                    inline=True
                )
            ])
        ])

spy_main = dbc.Card([
        dbc.CardBody([
                dbc.Label('Ventana Información: '),
                dbc.RadioItems(
                        value='1Y',
                        options=[
                                {'label' : '1M', 'value' : '1M'},
                                {'label' : '3M', 'value' : '3M'},
                                {'label' : '6M', 'value' : '6M'},
                                {'label' : '1Y', 'value' : '1Y'},
                                {'label' : '5Y', 'value' : '5Y'}
                                ],
                        id='freq-acc',
                        inline=True
                        ),
                dbc.Row(dbc.Col(html.Div(html.Br()))),
                dbc.Row([
                        dbc.Col(ind_1, width=6),
                        dbc.Col(ind_2, width=6)
                        ]),
                dcc.Graph(id='graf-acc'),
                ])
        ])

spy = html.Div([
        dbc.Row(dbc.Col(html.Div(html.Br()))),
        dbc.Row([
                dbc.Col(html.H4('Fecha de Corte: '), width={'size' : 'auto', 'offset' : 1}),
                dbc.Col(dcc.DatePickerSingle(id='fecha-acc',
                                             date = ultDiaHabil(),
                                             min_date_allowed = dt.date(2009, 1, 1),
                                             max_date_allowed = ultDiaHabil(),
                                             display_format = 'D/M/Y',
                                             persistence=False), width='auto'),
                dbc.Col(html.H4('Acción: '), width='auto'),
                dbc.Col(dcc.Dropdown(id='stock',
                                     value='^GSPC',
                                     options=[{'label' : i, 'value' : dict_acc[i]} for i in dict_acc.keys()]),
                                             width=4)
                ], justify='start'),
        dbc.Row(dbc.Col(html.Div(html.Br()))),
        dbc.Row([
                dbc.Col(spy_main, width={'size' : 10, 'offset' : 1}),
                ]),
        ])

#------------------------------------------------------------------------------
layout = html.Div([
        dbc.Row([
                dbc.Col(html.Div(html.H1("Dashboard Información Mercado")), width=10),
                ], justify = 'center'),
        dbc.Row(dbc.Col(html.Div(html.Br()))),
        dbc.Tabs([
                dbc.Tab(trm_oil, label='TRM y Petróleo', tab_style={'margin-left' : 'auto'}),
                dbc.Tab(spy, label='S&P 500'),
                ]),
        dbc.Row(dbc.Col(html.Div(html.Br()))),
        dbc.Row([
                dbc.Col(html.Div(html.Footer('Tomás Vergara Cardona - tomvc94@gmail.com')), width=10)
                ], justify = 'center')
        ])

app.layout = layout

#Callbacks Tab 1---------------------------------------------------------------

#Grafica TRM y Petroleo - Grafica Correlacion

def fig_trm_oil(df, freq):
    fig = make_subplots(specs=[[{'secondary_y' : True}]])
    
    fig.add_trace(
            go.Scatter(
                    x = df.index,
                    y = df.TRM,
                    name = 'TRM ' + freq),
            secondary_y = False
                    )
    
    fig.add_trace(
            go.Scatter(
                    x = df.index,
                    y = df.OIL,
                    name = 'Petróleo ' + freq),
            secondary_y = True
                    )
    
    fig.update_layout(title_text = 'Evolución {} TRM y Petróleo'.format(freq),
                      yaxis_tickformat = '$')
    
    fig.update_xaxes(title_text='Fecha')
    
    fig.update_yaxes(title_text='<b>TRM (COP)</b>',secondary_y=False)
    fig.update_yaxes(title_text='<b>Petróleo($USD/Barril)</b>', tickformat='$', secondary_y=True)
    return fig

@app.callback([Output('graf', 'figure'), Output('corr', 'figure')],
               [Input('fecha_corte', 'date'), Input('freq', 'value'), Input('date-corr', 'date')])

def graf_trm_oil(fecha, freq, fi):
    if fecha is not None:
        fecha = dt.datetime(int(fecha[:4]), int(fecha[5:7]), int(fecha[8:10]), 0, 0, 0)
    if fi is not None:
        fi = dt.datetime(int(fi[:4]), int(fi[5:7]), int(fi[8:10]), 0, 0, 0)
    #Traer Data   
    df_trm = get_TRM(fecha)
    df_oil = get_data('CL=F', dt.datetime(2008, 1, 1, 0, 0, 0), fecha)
    df_oil = df_oil.loc[:, ['Date', 'Close']]
    df_oil.columns = ['Fecha', 'OIL']
    df = pd.merge(df_trm, df_oil, how='left')
    df.fillna(method='bfill', inplace=True)
    df.set_index('Fecha', inplace=True)
    
    #Grafica principal
    if freq == 'Mensual':
        dfm = df.sort_index().resample('M').apply(lambda x: x.iloc[-1,])
        i = dfm.index.tolist()
        i[-1] = fecha
        dfm.index = i
        fig = fig_trm_oil(dfm, freq)
    elif freq == 'Anual':
        dfy = df.sort_index().resample('Y').apply(lambda x: x.iloc[-1,])
        i = dfy.index.tolist()
        i[-1] = fecha
        dfy.index = i
        fig = fig_trm_oil(dfy, freq)
    else:
        fig = fig_trm_oil(df, freq)
    
    #Grafica Correlacion
    df = df[df.index >= fi]
    
    df['rTRM'] = np.log(df['TRM'] / df['TRM'].shift(1))
    df['rOIL'] = np.log(df['OIL'] / df['OIL'].shift(1))
    
    c = df['rTRM'].corr(df['rOIL'])
    
    fig2 = px.scatter(
            x=df['rTRM'],
            y=df['rOIL'],            
            trendline='ols',
            trendline_color_override='red'
            )
    
    fig2.update_layout(title_text = 'Correlación TRM vs Petróleo: {:.3}'.format(c))
    fig2.update_xaxes(title_text='<b>TRM</b>', tickformat='%')
    fig2.update_yaxes(title_text='<b>Petróleo</b>',tickformat='%')
    
    return fig, fig2

#Boxplot TRM Mensual

@app.callback(Output('trm-box', 'figure'), [Input('fecha_corte', 'date')])

def trm_boxplot(fecha):
    df = get_TRM_BoxPlot(fecha)
    ma = list(df['MA'].unique())
    fig = go.Figure(data=[
            go.Box(
                    y = df[df['MA'] == i]['TRM'],
                    name=str(i)
                    ) for i in ma
            ])
    fig.update_layout(
            title_text='Boxplot Mensual TRM desde 2010',
            showlegend=False
            )
    fig.update_yaxes(title_text='<b>TRM (COP)</b>', tickformat='$')
    return fig

#Tabla con el Resumen Anual de TRM

@app.callback([Output('trm-table', 'data'), Output('trm-table', 'columns')],
               [Input('fecha_corte', 'date')])

def trm_year_table(fecha):
    if fecha is not None:
        fecha = dt.datetime(int(fecha[:4]), int(fecha[5:7]), int(fecha[8:10]), 0, 0, 0)
    df = trm_table_yr(fecha)
    return df.to_dict('rows'), [{'name' : i, 'id' : i} for i in df.columns]
#------------------------------------------------------------------------------

#Callbacks Tab 2---------------------------------------------------------------
dict_v = {'1M' : 30, '3M' : 90, '6M' : 180, '1Y' : 365, '5Y' : 365*5}

@app.callback(Output('graf-acc', 'figure'),
              [Input('fecha-acc', 'date'), Input('stock', 'value'), Input('freq-acc', 'value'),
               Input('ind-1', 'value'), Input('ind-2', 'value')])

def graf_stock(fecha, nemo, v, ind1, ind2):
    if fecha is not None:
        fecha = dt.datetime(int(fecha[:4]), int(fecha[5:7]), int(fecha[8:10]), 0, 0, 0)
    fecha_inicial = fecha - dt.timedelta(days=dict_v[v])
#    nemo = dict_acc[nemo]
    df = df_stocks(nemo, fecha, fecha_inicial, ind1, ind2)
    df = df[df.Date >= fecha_inicial]
    fig = make_subplots(rows=3, cols=1, row_heights=[0.5, 0.3, 0.2], 
                        shared_xaxes=True, vertical_spacing=0.02)
    
    cols = []
    for i in ind1:
        if i == 'BB':
            cols.append('BB+')
            cols.append('BB-')
        else:
            cols.append(i)
    
    #Grafica Principal
    fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Close'],
            name=nemo
            ), row=1, col=1)
    
    if len(cols) > 0:
        for col in cols:
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df[col],
                name=col
            ), row=1, col=1)
    
    #Grafica 2
    fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[ind2],
            name=ind2
            ), row=2, col=1)
    
    if ind2 == 'MACD':
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['MACD_Signal'],
            name='MACD_Signal'
            ), row=2, col=1)
    elif ind2 == 'Stochastic Oscillator':
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['SO_SMA'],
            name='SO_SMA'
            ), row=2, col=1)
    elif ind2 == 'RSI':
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=[70] * df.shape[0],
            name='Overbougth > 70 (RSI)',
            line=(dict(color='firebrick', dash='dot'))
            ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=[30] * df.shape[0],
            name='Oversold < 30 (RSI)',
            line=(dict(color='firebrick', dash='dot'))
            ), row=2, col=1)
    
    #Grafica 3
    fig.add_trace(go.Bar(
            x=df['Date'],
            y=df['Volume'],
            name='Volúmen'
            ), row=3, col=1)
    
    fig.update_layout(height=600)
    
    fig.update_yaxes(title_text=nemo, tickformat='$', row=1, col=1)
    fig.update_yaxes(title_text=ind2, row=2, col=1)
    fig.update_yaxes(title_text='Volúmen', tickformat='$', row=3, col=1)
    
    return fig

#------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(host='0.0.0.0',debug=True, port=8050)