from dash import html, dcc
import dash_bootstrap_components as dbc

from dash import html
from dash import dash_table

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from glob import glob
import os

from config import fnf_stations, fnf_id_names, df_system_status, graph_config

#fcst_t1  = date(2023, 4, 1)
#fcst_t2  = date(2023, 9, 30)
fcst_t1 = datetime.fromisoformat(df_system_status['ESP-WWRF-CCA Forecast'][0]).date()
fcst_t2 = datetime.fromisoformat(df_system_status['ESP-WWRF-CCA Forecast'][1]).date()
fcst_type0 = 'esp_wwrf_lstm'
staid0     = 'FTO'
staname0   = 'Feather River at Oroville'

# find all forecasts in the current year
tup1 = datetime(fcst_t1.year, 1, 1)
tup2 = datetime(fcst_t1.year, 7, 31)
dt_updates = [datetime.strptime(os.path.basename(d).split('_')[-1], 'update%Y%m%d') for d in glob(f'data/forecast/{fcst_type0}_init{fcst_t1.year}*_update*')]
dt_updates.sort()
tup_latest = dt_updates[-1]
#print(dt_updates)

## build time series figures
base_url = ''

# flow reanalysis figure
def draw_reana(staid):
    if staid in fnf_stations:
        fcsv = f'{base_url}data/reanalysis/{staid}.csv'
        df = pd.read_csv(fcsv, parse_dates=True, index_col='Date', names=['Date', 'FNF', 'Qsim', 'QsimBC'])
        fig_reana = px.line(df, labels={'Date': '', 'value': 'Flow (kaf/mon)'})
    else:
        fig_reana = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': 'Flow (kaf/mon)'})
    fig_reana.update_layout(margin=dict(l=15, r=15, t=15, b=5), plot_bgcolor='#eeeeee', legend=dict(title=''), hovermode='x unified') #, font=dict(size=20))
    fig_reana.update_traces(hovertemplate=None)
    return fig_reana
    
# flow monitor/forecast figure
def draw_mofor(staid, fcst_type, fcst_update):
    if staid in fnf_stations:
        fcsv = f'{base_url}data/forecast/{fcst_type}_init{fcst_t1:%Y%m%d}_update{fcst_update:%Y%m%d}/{staid}_{fcst_t1:%Y%m%d}-{fcst_t2:%Y%m%d}.csv'
        df = pd.read_csv(fcsv, parse_dates=True, index_col='Date', usecols = ['Date']+['Ens%02d' % (i+1) for i in range(42)]+['Avg', 'Exc50', 'Exc90', 'Exc10'])
        df.drop(index=df.index[-1], axis=0, inplace=True)
        linecolors = {'Ens%02d' % (i+1): 'lightgray' for i in range(42)}
        linecolors.update({'Avg': 'black', 'Exc50': 'green', 'Exc90': 'red', 'Exc10': 'blue'})
        fig_mofor = px.line(df, labels={'Date': '', 'value': 'Flow (kaf/mon)'}, color_discrete_map=linecolors, markers=True)
    else:
        fig_mofor = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': 'Flow (kaf/mon)'})
    fig_mofor.update_layout(margin=dict(l=15, r=15, t=15, b=5), plot_bgcolor='#eeeeee', legend=dict(title=''), hovermode='x unified')
    fig_mofor.update_traces(hovertemplate=None)
    return fig_mofor
    
# ancillary data figure
def draw_ancil(staid):
    if staid!=None:
        fig_ancil = px.line(x=[2018, 2023], y=[50, 50], labels={'x': 'Time', 'y': 'Percentile'})
    else:
        fig_ancil = px.line(x=[2018, 2023], y=[50, 50], labels={'x': 'Data not available.', 'y': 'Percentile'})
    fig_ancil.update_layout(margin=dict(l=15, r=15, t=15, b=5), plot_bgcolor='#eeeeee')
    return fig_ancil

table_note = html.Div('  [Note] 50%, 90%, 10%: exceedance levels within the forecast ensemble. AVG: month of year average during 1979-2020. %AVG: percentage of AVG. KAF: kilo-acre-feet.', id='table-note', style={'font-size': 'small'})

# forecast table
def draw_table(staid, staname, fcst_type, fcst_update):
    cols = ['Date', 'Exc50', 'Pav50', 'Exc90', 'Pav90', 'Exc10', 'Pav10', 'Avg']
    if staid in fnf_stations:
        fcsv = f'{base_url}data/forecast/{fcst_type}_init{fcst_t1:%Y%m%d}_update{fcst_update:%Y%m%d}/{staid}_{fcst_t1:%Y%m%d}-{fcst_t2:%Y%m%d}.csv'
        df = pd.read_csv(fcsv, parse_dates=False, usecols=cols)
        df = df[cols]
        cols.remove('Date')
        df[cols] = np.rint(df[cols])
        df['Date'] = [ datetime.strptime(m, '%Y-%m-%d').strftime('%B %Y') for m in df['Date'] ]
        df.iloc[-1, 0] = df.iloc[-1, 0].replace('July', 'April-July total')
    else:
        fcsv = f'{base_url}data/forecast/{fcst_type}_init{fcst_t1:%Y%m%d}_update{fcst_update:%Y%m%d}/FTO_{fcst_t1:%Y%m%d}-{fcst_t2:%Y%m%d}.csv'
        df = pd.read_csv(fcsv, parse_dates=False, usecols=cols)
        df = df[cols]
        df.drop(df.index, inplace=True)

    #df.rename(columns={'Date': 'Month', 'Exc50': '50% (KAF)', 'Pav50': '50% (%AVG)', 'Exc90': '90% (KAF)', 'Pav90': '90% (%AVG)', 'Exc10': '10% (KAF)', 'Pav10': '10% (%AVG)', 'Avg': 'AVG (KAF)'}, inplace=True)
    table_fcst = dash_table.DataTable(id='fcst-table',
                     #columns=[{'name': i, 'id': i} for i in df.columns],
                     columns=[{'name': [staname, 'Month'], 'id': 'Date'},
                              {'name': ['50%', 'KAF'], 'id': 'Exc50'}, {'name': ['50%', '%AVG'], 'id': 'Pav50'},
                              {'name': ['90%', 'KAF'], 'id': 'Exc90'}, {'name': ['90%', '%AVG'], 'id': 'Pav90'},
                              {'name': ['10%', 'KAF'], 'id': 'Exc10'}, {'name': ['10%', '%AVG'], 'id': 'Pav10'},
                              {'name': ['AVG', 'KAF'], 'id': 'Avg'}
                              ],
                     data=df.to_dict('records'),
                     style_data={'whiteSpace': 'normal', 'width': '300px'},
                     style_header={'backgroundColor': 'lightyellow', 'fontWeight': 'bold', 'textAlign': 'center'},
                     style_table={'padding-bottom': '0px'},
                     export_format='xlsx',
                     export_headers='display',
                     merge_duplicate_headers=True,
                     )

    return [table_fcst, table_note]

# forecast tables over all FNF stations
def draw_table_all(fcst_type, fcst_update):
    cnt = 0
    for staid,staname in fnf_id_names.items():
        cols = ['Date', 'Exc50', 'Pav50', 'Exc90', 'Pav90', 'Exc10', 'Pav10', 'Avg']
        fcsv = f'{base_url}data/forecast/{fcst_type}_init{fcst_t1:%Y%m%d}_update{fcst_update:%Y%m%d}/{staid}_{fcst_t1:%Y%m%d}-{fcst_t2:%Y%m%d}.csv'
        df = pd.read_csv(fcsv, parse_dates=False, usecols=cols)
        df = df[cols]
        cols.remove('Date')
        df[cols] = np.rint(df[cols])
        df['Date'] = [ datetime.strptime(m, '%Y-%m-%d').strftime('%B %Y') for m in df['Date'] ]
        df.iloc[-1, 0] = df.iloc[-1, 0].replace('July', 'April-July total')
        #df.insert(loc=0, column='Station', value=[staname if i==0 else '' for i in range(df.shape[0])])
        df.loc[-1] = ['' if i>0 else staname for i in range(df.shape[1])]
        df.index = df.index + 1  # shifting index
        df.sort_index(inplace=True) 
        if cnt==0:
            df_all = df
        else:
            df_all = df_all.append(df, ignore_index=True)
        cnt += 1
    #df_all.drop(df_all.tail(1).index, inplace=True)
    table_fcst = dash_table.DataTable(id='fcst-table',
                     #columns=[{'name': i, 'id': i} for i in df.columns],
                     columns=[
                              #{'name': ['', 'Station (%d in total)' % cnt], 'id': 'Station'},
                              {'name': ['Station', 'Month'], 'id': 'Date'},
                              {'name': ['50%', 'KAF'], 'id': 'Exc50'}, {'name': ['50%', '%AVG'], 'id': 'Pav50'},
                              {'name': ['90%', 'KAF'], 'id': 'Exc90'}, {'name': ['90%', '%AVG'], 'id': 'Pav90'},
                              {'name': ['10%', 'KAF'], 'id': 'Exc10'}, {'name': ['10%', '%AVG'], 'id': 'Pav10'},
                              {'name': ['AVG', 'KAF'], 'id': 'Avg'}
                              ],
                     data=df_all.to_dict('records'),
                     style_data={'whiteSpace': 'normal', 'maxWidth': '400px'},
                     style_cell={'whiteSpace': 'normal', 'minWidth': '100px'},
                     style_header={'backgroundColor': 'lightyellow', 'fontWeight': 'bold', 'textAlign': 'center'},
                     style_table={'padding-bottom': '0px'},
                     export_format='xlsx',
                     export_headers='display',
                     merge_duplicate_headers=True,
                     page_size=df.shape[0],
                     page_current=0,
                     )

    return [table_fcst]

## pop-up window and its tabs/graphs/tables

fig_reana = draw_reana(staid0)
fig_mofor = draw_mofor(staid0, fcst_type0, tup_latest)
fig_ancil = draw_ancil(staid0)

table_fcst = draw_table(staid0, staname0, fcst_type0, tup_latest)

graph_reana = dcc.Graph(id='graph-reana', figure=fig_reana, style={'height': '360px'}, config=graph_config)
graph_mofor = dcc.Graph(id='graph-mofor', figure=fig_mofor, style={'height': '360px'}, config=graph_config)
graph_ancil = dcc.Graph(id='graph-ancil', figure=fig_ancil, style={'height': '360px'}, config=graph_config)
div_table = html.Div(id='div-table', children=table_fcst, style={'padding': '0px 50px 30px 50px', 'maxHeight': '350px', 'overflowY': 'scroll'})


tabtitle_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
tabtitle_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

tab_reana = dcc.Tab(label='Reanalysis',      value='reana', children=[dcc.Loading(id='loading-reana', children=graph_reana)], style=tabtitle_style, selected_style=tabtitle_selected_style)
tab_mofor = dcc.Tab(label='Monitor/Forecast',value='mofor', children=[dcc.Loading(id='loading-mofor', children=graph_mofor)], style=tabtitle_style, selected_style=tabtitle_selected_style)
tab_ancil = dcc.Tab(label='Ancillary Data',  value='ancil', children=[dcc.Loading(id='loading-ancil', children=graph_ancil)], style=tabtitle_style, selected_style=tabtitle_selected_style)
tab_table = dcc.Tab(label='Table',           value='table', children=[dcc.Loading(id='loading-table', children=div_table)],   style=tabtitle_style, selected_style=tabtitle_selected_style)

#popup_tabs = dcc.Tabs([tab_mofor, tab_table, tab_reana, tab_ancil], id='popup-tabs', value='mofor')
popup_tabs = dcc.Tabs([tab_mofor, tab_table, tab_reana], id='popup-tabs', value='mofor')

slider_updates = dcc.Slider(min=tup1.timetuple().tm_yday, max=tup2.timetuple().tm_yday, step=None,
    marks={dt.timetuple().tm_yday: dt.strftime('%-m/%-d') for dt in dt_updates},
    value=tup_latest.timetuple().tm_yday,
    id='slider_updates'
)

slider_text  = html.Div('Forecast Updated on:', style={'display': 'inline-block', 'font-weight': 'bold', 'vertical-align': 'top'})
slider_block = html.Div(slider_updates, style={'width': '70%', 'display': 'inline-block'})

radio_pp = dcc.RadioItems(
   options=[
       {'label': 'CDF Match', 'value': 'cdf'},
       {'label': 'LSTM',      'value': 'lstm'},
   ],
   value='lstm', labelStyle={'padding-right': 10}, id='radio_pp'
)

radio_text  = html.Div('Post-Processing: ', style={'display': 'inline-block', 'font-weight': 'bold', 'vertical-align': 'top', 'padding-right': 10})
radio_block = html.Div(radio_pp, style={'vertical-align': 'top', 'display': 'inline-block'})

popup_plots = dbc.Offcanvas([slider_text, slider_block, radio_text, radio_block, popup_tabs],
    title='B-120 Forecast Point', placement='top', is_open=False, scrollable=True, id='popup-plots',
    style={'opacity': '0.9', 'width': '90%', 'min-width': '1000px', 'min-height': '540px', 'margin-top': '150px', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': 'smaller'}
)
