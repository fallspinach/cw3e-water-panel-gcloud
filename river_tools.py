from dash import html, dcc
import dash_bootstrap_components as dbc

from dash import html
from dash import dash_table

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import sqlite3
import numpy as np
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

curr_day = datetime.utcnow().date()
moni_t1  = curr_day - timedelta(days=curr_day.day-1) - relativedelta(months=2)
moni_t2  = moni_t1 + relativedelta(months=6)-timedelta(days=1)
moni_t1  = date(2022, 10,  1)
moni_t2  = date(2023,  3,  1)
fcst_t1  = date(2023,  3, 29)
fcst_t2  = date(2023,  4,  6)
#fcst_type = 'fusion'
fcst_type = 'wwrf'


## build time series figures
base_url = 'https://cw3e.ucsd.edu/wrf_hydro/cnrfc/' # easier to update the data but slow to load
base_url = ''

    
# flow monitor/forecast figure
def draw_mofor_river(rivid):
    if rivid != '':
        fig_mofor = go.Figure()
        
        fillcolors = ['sienna', 'orange', 'yellow', 'lightgreen', 'lightcyan', 'lightblue', 'mediumpurple']
        fillcolors.reverse()
        for i,pctl in enumerate([95, 90, 80, 50, 20, 10, 5]):
            fcsv = base_url + 'data/monitor/CHRTOUT_%s-%s.daily.pctl%02d.csv.gz' % (moni_t1.strftime('%Y%m'), fcst_t2.strftime('%Y%m'), pctl)
            df = pd.read_csv(fcsv, parse_dates=True, usecols = ['Date', str(rivid)])
            num = df._get_numeric_data(); num[num<0] = 0
            df.rename(columns={str(rivid): 'Flow'}, inplace=True)
            tsname = '  %d<sup>th</sup>' % pctl if pctl<10 else '%d<sup>th</sup>' % pctl
            fig_mofor.add_trace(go.Scatter(x=df['Date'], y=df['Flow'], name=tsname, line=dict(color=fillcolors[i]), fill='tozeroy', mode='lines'))
        
        fcsv = base_url + 'data/monitor/CHRTOUT_%s-%s.daily.csv.gz' % (moni_t1.strftime('%Y%m'), moni_t2.strftime('%Y%m'))
        df = pd.read_csv(fcsv, parse_dates=True, usecols = ['Date', str(rivid)])
        num = df._get_numeric_data(); num[num<0] = 0
        df.rename(columns={str(rivid): 'Flow'}, inplace=True)
        #fig_mofor.add_trace(go.Scatter(x=df['Date'], y=df['Flow'], name='Monitor', line=dict(color='blue'), mode='lines+markers'))
        df2 = df.tail(1)
        
        fcsv = base_url + 'data/monitor/CHRTOUT_%s-%s.daily.csv.gz' % (fcst_t1.strftime('%Y%m%d'), fcst_t2.strftime('%Y%m%d'))
        dff = pd.read_csv(fcsv, parse_dates=True, usecols = ['Date', str(rivid)])
        num = dff._get_numeric_data(); num[num<0] = 0
        dff.rename(columns={str(rivid): 'Flow'}, inplace=True)
        dff = pd.concat([df2, dff]).reset_index(drop = True)
        fig_mofor.add_trace(go.Scatter(x=dff['Date'], y=dff['Flow'], name='Forecast', line=dict(color='magenta'), mode='lines+markers'))
        fig_mofor.add_trace(go.Scatter(x=df['Date'], y=df['Flow'], name='Monitor', line=dict(color='blue'), mode='lines+markers'))
        
    else:
        fig_mofor = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': 'Flow (m^3/s)'})
    fig_mofor.update_layout(margin=dict(l=15, r=15, t=15, b=5), plot_bgcolor='#eeeeee', legend=dict(title=''), hovermode='x unified',
                            xaxis_title='Forecast Initiated on %s' % fcst_t1.strftime('%b %d, %Y'),
                            yaxis_title='Model Estimated Flow (m<sup>3</sup>/s, <b>uncorrected</b>)')
    fig_mofor.update_traces(hovertemplate=None)
    return fig_mofor
    
# flow monitor/forecast figure
def draw_mofor_river_db(rivid):
    if rivid != '':
        fig_mofor = go.Figure()
        
        fillcolors = ['sienna', 'orange', 'yellow', 'lightgreen', 'lightcyan', 'lightblue', 'mediumpurple']
        fillcolors.reverse()
        for i,pctl in enumerate([95, 90, 80, 50, 20, 10, 5]):
            fdb = base_url + 'data/monitor/CHRTOUT_%s-%s.daily.pctl%02d.db' % (moni_t1.strftime('%Y%m'), fcst_t2.strftime('%Y%m'), pctl)
            conn = sqlite3.connect(fdb)
            df = pd.read_sql_query('SELECT * FROM streamflow WHERE [index]=%s' % str(rivid), conn).T
            conn.close()
            df.drop(index=df.index[0], axis=0, inplace=True)
            num = df._get_numeric_data(); num[num<0] = 0
            df.rename(columns={0: 'Flow'}, inplace=True)
            tsname = '  %d<sup>th</sup>' % pctl if pctl<10 else '%d<sup>th</sup>' % pctl
            fig_mofor.add_trace(go.Scatter(x=df.index, y=df['Flow'], name=tsname, line=dict(color=fillcolors[i]), fill='tozeroy', mode='lines'))
        
        fdb = base_url + 'data/monitor/CHRTOUT_%s-%s.daily.db' % (moni_t1.strftime('%Y%m'), moni_t2.strftime('%Y%m'))
        conn = sqlite3.connect(fdb)
        df = pd.read_sql_query('SELECT * FROM streamflow WHERE [index]=%s' % str(rivid), conn).T
        conn.close()
        df.drop(index=df.index[0], axis=0, inplace=True)
        num = df._get_numeric_data(); num[num<0] = 0
        df.rename(columns={0: 'Flow'}, inplace=True)
        #fig_mofor.add_trace(go.Scatter(x=df['Date'], y=df['Flow'], name='Monitor', line=dict(color='blue'), mode='lines+markers'))
        df2 = df.tail(1)
        
        fdb = base_url + 'data/monitor/CHRTOUT_%s-%s.daily.db' % (fcst_t1.strftime('%Y%m%d'), fcst_t2.strftime('%Y%m%d'))
        conn = sqlite3.connect(fdb)
        dff = pd.read_sql_query('SELECT * FROM streamflow WHERE [index]=%s' % str(rivid), conn).T
        conn.close()
        dff.drop(index=dff.index[0], axis=0, inplace=True)
        num = dff._get_numeric_data(); num[num<0] = 0
        dff.rename(columns={0: 'Flow'}, inplace=True)
        dff = pd.concat([df2, dff])#.reset_index(drop = True)
        fig_mofor.add_trace(go.Scatter(x=dff.index, y=dff['Flow'], name='Forecast', line=dict(color='magenta'), mode='lines+markers'))
        fig_mofor.add_trace(go.Scatter(x=df.index, y=df['Flow'], name='Monitor', line=dict(color='blue'), mode='lines+markers'))
        
    else:
        fig_mofor = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': 'Flow (m^3/s)'})
    fig_mofor.update_layout(margin=dict(l=15, r=15, t=15, b=5), plot_bgcolor='#eeeeee', legend=dict(title=''), hovermode='x unified',
                            xaxis_title='Forecast Initiated on %s' % fcst_t1.strftime('%b %d, %Y'),
                            yaxis_title='Model Estimated Flow (m<sup>3</sup>/s, <b>uncorrected</b>)')
    fig_mofor.update_traces(hovertemplate=None)
    return fig_mofor
    
fig_mofor_river = draw_mofor_river_db('342455')

graph_mofor_river = dcc.Graph(id='graph-mofor-river', figure=fig_mofor_river, style={'height': '360px'})

tabtitle_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
tabtitle_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

tab_mofor_river = dcc.Tab(label='Monitor/Forecast',value='mofor-river', children=[dcc.Loading(id='loading-mofor-river', children=graph_mofor_river)], style=tabtitle_style, selected_style=tabtitle_selected_style)

popup_tabs_river = dcc.Tabs([tab_mofor_river], id='popup-tabs-river', value='mofor-river')

popup_plots_river = dbc.Offcanvas(
    [popup_tabs_river],
    title='WRF-Hydro Forecast Point', placement='top', is_open=False, scrollable=True, id='popup-plots-river',
    style={'opacity': '0.9', 'width': '90%', 'min-width': '1000px', 'min-height': '500px', 'margin-top': '150px', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': 'smaller'}
)
