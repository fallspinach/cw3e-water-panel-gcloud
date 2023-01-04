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

curr_day = datetime.utcnow().date()
fcst_t1  = curr_day - timedelta(days=curr_day.day-1) - relativedelta(months=2)
fcst_t1  = date(2022, 7, 1)
fcst_t2  = fcst_t1 + relativedelta(months=6)-timedelta(days=1)
#fcst_type = 'fusion'
fcst_type = 'esp'

all_stations = {'AMF': 'American River below Folsom Lake', 'ASP': 'Arroyo Seco near Pasadena', 'ASS': 'Arroyo Seco near Soledad', 'CSN': 'Cosumnes River at Michigan Bar', 'EFC': 'East Carson near Gardnerville', 'EWR': 'East Walker near Bridgeport', 'ERS': 'Eel River at Scotia', 'FTO': 'Feather River at Oroville', 'KWT': 'Kaweah River below Terminus reservoir', 'KRB': 'Kern River below City of Bakersfield', 'KRI': 'Kern River below Lake Isabella', 'KGF': 'Kings River below Pine Flat reservoir', 'KLO': 'Klamath River Copco to Orleans', 'MSS': 'McCloud River above Shasta Lake', 'MRC': 'Merced River below Merced Falls', 'MKM': 'Mokelumne River inflow to Pardee', 'NCD': 'Nacimiento below Nacimiento Dam', 'NPH': 'Napa River near St Helena', 'OWL': 'Owens River below Long Valley Dam', 'PSH': 'Pit River near Montgomerey and Squaw Creek', 'RRH': 'Russian River at Healdsburg', 'SBB': 'Sacramento R above Bend Bridge', 'SDT': 'Sacramento River at Delta', 'SRS': 'Salmon River at Somes Bar', 'SJF': 'San Joaquin River below Millerton Lake', 'ANM': 'Santa Ana River near Mentone', 'SSP': 'Sespe Creek near Fillmore', 'SIS': 'Shasta Lake Total Inflow', 'SNS': 'Stanislaus River below Goodwin', 'TNL': 'Trinity River near Lewiston Lake', 'TRF': 'Truckee River from Tahoe to Farad', 'SCC': 'Tule River below Lake Success', 'TLG': 'Tuolumne River below Lagrange reservoir', 'WFC': 'West Fork Carson at Woodfords', 'WWR': 'West Walker near Coleville', 'YRS': 'Yuba River near Smartsville'}

fnf_stations = ['AMF', 'CSN', 'EFC', 'EWR', 'FTO', 'KGF', 'KRI', 'KWT', 'MKM', 'MRC', 'MSS', 'PSH', 'SBB', 'SCC', 'SDT', 'SIS', 'SJF', 'SNS', 'TLG', 'TNL', 'TRF', 'WFC', 'WWR', 'YRS']
fnf_stations = ['TNL', 'SDT', 'MSS', 'PSH', 'SIS', 'SBB', 'FTO', 'YRS', 'AMF', 'CSN', 'MKM', 'SNS', 'TLG', 'MRC', 'SJF', 'KGF', 'KWT', 'SCC', 'KRI', 'TRF', 'WFC', 'EFC', 'WWR', 'EWR']

fnf_id_names = {key: all_stations[key] for key in fnf_stations}

## build time series figures

# flow reanalysis figure
def draw_reana(staid):
    if staid in fnf_stations:
        fcsv = 'data/reanalysis/%s.csv' % staid
        df = pd.read_csv(fcsv, parse_dates=True, index_col='Date', names=['Date', 'FNF', 'Qsim', 'QsimBC'])
        fig_reana = px.line(df, labels={'Date': '', 'value': 'Flow (kaf/mon)'})
    else:
        fig_reana = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': 'Flow (kaf/mon)'})
    fig_reana.update_layout(margin=dict(l=15, r=15, t=15, b=5))
    return fig_reana
    
# flow monitor/forecast figure
def draw_mofor(staid):
    if staid in fnf_stations:
        fcsv = 'data/forecast/%s_%s/%s_%s-%s.csv' % (fcst_type, fcst_t1.strftime('%Y%m%d'), staid, fcst_t1.strftime('%Y%m%d'), fcst_t2.strftime('%Y%m%d'))
        df = pd.read_csv(fcsv, parse_dates=True, index_col='Date', usecols = ['Date']+['Ens%02d' % (i+1) for i in range(42)]+['Avg', 'Exc50', 'Exc90', 'Exc10'])
        df.drop(index=df.index[-1], axis=0, inplace=True)
        linecolors = {'Ens%02d' % (i+1): 'lightgray' for i in range(42)}
        linecolors.update({'Avg': 'black', 'Exc50': 'green', 'Exc90': 'red', 'Exc10': 'blue'})
        fig_mofor = px.line(df, labels={'Date': '', 'value': 'Flow (kaf/mon)'}, color_discrete_map=linecolors, markers=True)
    else:
        fig_mofor = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': 'Flow (kaf/mon)'})
    fig_mofor.update_layout(margin=dict(l=15, r=15, t=15, b=5))
    return fig_mofor
    
# ancillary data figure
def draw_ancil(staid):
    if staid!=None:
        fig_ancil = px.line(x=[2018, 2023], y=[50, 50], labels={'x': 'Time', 'y': 'Percentile'})
    else:
        fig_ancil = px.line(x=[2018, 2023], y=[50, 50], labels={'x': 'Data not available.', 'y': 'Percentile'})
    return fig_ancil

table_note = html.Div('  [Note] 50%, 90%, 10%: exceedance levels within the forecast ensemble. AVG: month of year average during 1979-2020. %AVG: percentage of AVG. KAF: kilo-acre-feet.', id='table-note')

# forecast table
def draw_table(staid, staname):
    cols = ['Date', 'Exc50', 'Pav50', 'Exc90', 'Pav90', 'Exc10', 'Pav10', 'Avg']
    if staid in fnf_stations:
        fcsv = 'data/forecast/%s_%s/%s_%s-%s.csv' % (fcst_type, fcst_t1.strftime('%Y%m%d'), staid, fcst_t1.strftime('%Y%m%d'), fcst_t2.strftime('%Y%m%d'))
        df = pd.read_csv(fcsv, parse_dates=False, usecols=cols)
        df = df[cols]
        cols.remove('Date')
        df[cols] = np.rint(df[cols])
        df['Date'] = [ datetime.strptime(m, '%Y-%m-%d').strftime('%B %Y') for m in df['Date'] ]
        df.iloc[-1, 0] = df.iloc[-1, 0].replace('July', 'April-July total')
    else:
        fcsv = 'data/forecast/%s_%s/FTO_%s-%s.csv' % (fcst_type, fcst_t1.strftime('%Y%m%d'), fcst_t1.strftime('%Y%m%d'), fcst_t2.strftime('%Y%m%d'))
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
def draw_table_all():
    cnt = 0
    for staid,staname in fnf_id_names.items():
        cols = ['Date', 'Exc50', 'Pav50', 'Exc90', 'Pav90', 'Exc10', 'Pav10', 'Avg']
        fcsv = 'data/forecast/%s_%s/%s_%s-%s.csv' % (fcst_type, fcst_t1.strftime('%Y%m%d'), staid, fcst_t1.strftime('%Y%m%d'), fcst_t2.strftime('%Y%m%d'))
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

fig_reana = draw_reana('FTO')
fig_mofor = draw_mofor('FTO')
fig_ancil = draw_ancil('FTO')

table_fcst = draw_table('FTO', 'Feather River at Oroville')

graph_reana = dcc.Graph(id='graph-reana', figure=fig_reana, style={'height': '360px'})
graph_mofor = dcc.Graph(id='graph-mofor', figure=fig_mofor, style={'height': '360px'})
graph_ancil = dcc.Graph(id='graph-ancil', figure=fig_ancil, style={'height': '360px'})
div_table = html.Div(id='div-table', children=table_fcst, style={'padding': '0px 50px 30px 50px', 'maxHeight': '350px', 'overflowY': 'scroll'})


tab_style = {'height': '28px', 'padding': '1px', 'margin': '0px'}

tab_reana = dcc.Tab(label='Reanalysis',      value='reana', children=[dcc.Loading(id='loading-reana', children=graph_reana)], style=tab_style, selected_style=tab_style)
tab_mofor = dcc.Tab(label='Monitor/Forecast',value='mofor', children=[dcc.Loading(id='loading-mofor', children=graph_mofor)], style=tab_style, selected_style=tab_style)
tab_ancil = dcc.Tab(label='Ancillary Data',  value='ancil', children=[dcc.Loading(id='loading-ancil', children=graph_ancil)], style=tab_style, selected_style=tab_style)
tab_table = dcc.Tab(label='Table',           value='table', children=[dcc.Loading(id='loading-table', children=div_table)],  style=tab_style, selected_style=tab_style)

popup_tabs = dcc.Tabs([tab_reana, tab_mofor, tab_ancil, tab_table], id='popup-tabs', value='reana', style=tab_style)

popup_plots = dbc.Offcanvas(
    [popup_tabs],
    title='B-120 Forecast Point', placement='top', is_open=False, scrollable=True, id='popup-plots',
    style={'opacity': '0.9', 'width': '90%', 'min-width': '1000px', 'min-height': '500px', 'margin-top': '150px', 'margin-left': 'auto', 'margin-right': 'auto'}
)
