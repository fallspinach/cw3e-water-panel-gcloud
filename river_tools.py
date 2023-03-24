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
fcst_t2  = fcst_t1 + relativedelta(months=6)-timedelta(days=1)
fcst_t1  = date(2022, 10, 1)
fcst_t2  = date(2023,  3, 1)
#fcst_type = 'fusion'
fcst_type = 'esp_wwrf'


## build time series figures
base_url = 'https://cw3e.ucsd.edu/wrf_hydro/cnrfc/' # easier to update the data but slow to load
base_url = ''

    
# flow monitor/forecast figure
def draw_mofor_river(staid):
    if staid != '':
        fcsv = base_url + 'data/monitor/CHRTOUT_%s-%s.daily.csv.gz' % (fcst_t1.strftime('%Y%m'), fcst_t2.strftime('%Y%m'))
        df = pd.read_csv(fcsv, parse_dates=True, index_col='Date', usecols = ['Date', str(staid)])
        fig_mofor = px.line(df, labels={'Date': '', 'value': 'Flow (m^3/s)'}, markers=True)
    else:
        fig_mofor = px.line(x=[2018, 2023], y=[0, 0], labels={'x': 'Data not available.', 'y': 'Flow (m^3/s)'})
    fig_mofor.update_layout(margin=dict(l=15, r=15, t=15, b=5), plot_bgcolor='#eeeeee', legend=dict(title=''), hovermode='x unified')
    fig_mofor.update_traces(hovertemplate=None)
    return fig_mofor
    
fig_mofor_river = draw_mofor_river('342455')

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
