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
#import pandas as pd
#import dash_table
#import plotly.graph_objects as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
suppress_callback_exceptions = True

from funciones import ultDiaHabil, get_TRM, get_data

graf_trm = dbc.Card([
        dbc.CardBody([
                html.H6('TRM', className='card-title'),
                dcc.Graph(id='trm')
                ])
        ])

graf_oil = dbc.Card([
        dbc.CardBody([
                html.H6('Petróleo', className='card-title'),
                dcc.Graph(id='oil')
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
                dbc.Col(graf_trm, width={'size' : 5, 'offset' : 1}),
                dbc.Col(graf_oil, width=5)
                ])
        ])

spy = html.Div(html.H1('Hola'))

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


if __name__ == "__main__":
    app.run_server(host='0.0.0.0',debug=True, port=8050)