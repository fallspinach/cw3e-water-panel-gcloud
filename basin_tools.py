from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import Namespace, arrow_function

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

from config import map_tiles, fnf_stations, fnf_id_names, df_system_status, graph_config

# start to build maps
ns = Namespace('dashExtensions', 'default')

# B-120 basin elevation bands
elev_scale = ['magenta', 'red', 'orangered', 'orange', 'yellow', 'yellowgreen', 'green', 'cyan', 'turquoise', 'blue', 'indigo', 'purple', 'violet', 'gray', 'lightgray', 'white']
elev_classes = [-1, 999, 1999, 2999, 3999, 4999, 5999, 6999, 7999, 8999, 9999, 10999, 11999, 12999, 13999, 14999]
elev_style = dict(weight=0, opacity=1, color='darkblue', fillOpacity=0.3)
elev_bands = dl.GeoJSON(url='assets/elev_bands_FTO.pbf', format='geobuf', id='elev-bands', zoomToBounds=True,
                        options=dict(style=ns('b120_style')),
                        hoverStyle=arrow_function(dict(weight=1, color='black', dashArray='', fillOpacity=0.5)),
                        hideout=dict(colorscale=elev_scale, classes=elev_classes, style=elev_style, colorProp='low_range'))
                        
# basin zoom-in map on the right
map_basin  = dl.Map([map_tiles[2], elev_bands],
                    center=[40, -121], zoom=8, zoomControl=False,
                    style={'width': '100%', 'height': '100%', 'min-height': '400px', 'min-width': '500px', 'margin': '0px', 'display': 'block'})

# draw precip climatology by elevation bands
base_url = 'https://cw3e.ucsd.edu/wrf_hydro/cnrfc/' # easier to update the data but slow to load
base_url = ''
def draw_precip_by_elev(staid):
    if staid in fnf_stations:
        fcsv = base_url + 'data/climatology/precip_by_elev/%s.csv' % (staid)
        df = pd.read_csv(fcsv, parse_dates=True, index_col='Date')
        linecolors = {'%d-%d' % (i*1000, i*1000+999): elev_scale[i] for i in range(16)}
        fig_precip_by_elev = px.line(df, labels={'Date': 'Date', 'value': 'Precipitation Depth (mm)'}, color_discrete_map=linecolors, markers=False)
    else:
        fig_precip_by_elev = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': 'Precipitation Depth (mm)'})
    fig_precip_by_elev.update_traces(hovertemplate=None)
    fig_precip_by_elev.update_layout(title='Historical Mean Precip until Jul 31, %s: %s' % (staid, fnf_id_names[staid]),
                                     margin=dict(l=15, r=15, t=35, b=5), plot_bgcolor='#eeeeee', title_font_size=15,
                                     legend=dict(yanchor='top', y=0.99, xanchor='right', x=0.99, title='Elev bands (ft)'),
                                     hovermode='x unified')
    fig_precip_by_elev.update_xaxes(dtick='M1', tickformat='%b %-d')
    return fig_precip_by_elev

fig_precip_by_elev = draw_precip_by_elev('FTO')
graph_precip_by_elev = dcc.Graph(id='graph-precip-by-elev', figure=fig_precip_by_elev, style={'height': '410px', 'padding-top': '10px'}, config=graph_config)

# tool panel
tool_style  = {'min-height': '412px', 'background-color': 'white', 'font-size': 'small'}
precip_by_elev_tab = html.Div([dcc.Loading(id='loading-precip-by-elev', children=graph_precip_by_elev)], style=tool_style)
snow_tab           = html.Div(['Snowpack and rain-on-snow risk analysis.'], style=tool_style)

# draw system status chart
base_url = 'https://cw3e.ucsd.edu/wrf_hydro/cnrfc/' # easier to update the data but slow to load
def draw_system_status():
    fig_system_status = go.Figure()
    i = 1
    for datastream,datatime in df_system_status.iteritems():
        if datastream not in ['Forcing BC', 'WRF-Hydro Reanalysis', 'Current']:
            fig_system_status.add_trace(go.Scatter(x=datatime, y=[i, i], name=datastream, 
                text=[datastream+' '+datetime.fromisoformat(datatime[0]).strftime('%-m/%-d %HZ'), datastream+' '+datetime.fromisoformat(datatime[1]).strftime('%-m/%-d %HZ')],
                                                   textposition='top center', line=dict(width=10), mode='lines+text'))
            i += 1
        if datastream=='Current':
            fig_system_status.add_trace(go.Scatter(x=datatime, y=[0.5, i-1], name=datastream, text=['Status Update @ '+datetime.fromisoformat(datatime[1]).strftime('%-m/%-d %HZ'), ''], line=dict(dash='dash'), mode='lines+text'))
            i += 1
    fig_system_status.update_traces(hovertemplate='%{x}')
    fig_system_status.update_layout(title='System Status', showlegend=False, xaxis_range=[datetime.utcnow()-timedelta(days=32), datetime.utcnow()+timedelta(days=10)],
                                    margin=dict(l=15, r=15, t=35, b=5), plot_bgcolor='#eeeeee', title_font_size=15,
                                    legend=dict(yanchor='top', y=0.99, xanchor='right', x=0.99, title='Datastream'))
    fig_system_status.update_xaxes(dtick='D', tickformat='%-m/%-d')
    fig_system_status.update_yaxes(visible=False)
    return fig_system_status

fig_system_status = draw_system_status()
graph_system_status = dcc.Graph(id='graph-system_status', figure=fig_system_status, style={'height': '410px', 'padding-top': '10px'}, config=graph_config)

# system status panel
system_status_tab = html.Div([dcc.Loading(id='loading-system-status', children=graph_system_status)], style=tool_style)

tab_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
tab_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

basin_tools = html.Div(dcc.Tabs([
    dcc.Tab([precip_by_elev_tab], label='Precipitation',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab([snow_tab],           label='Snowpack',       style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder 1'], style=tool_style), label='Soil Moisture',    style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder X'], style=tool_style), label='Tool X',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder Y'], style=tool_style), label='Tool Y',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder Z'], style=tool_style), label='Tool Z',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab([system_status_tab],  label='System Status',  style=tab_style, selected_style=tab_selected_style),
]))

