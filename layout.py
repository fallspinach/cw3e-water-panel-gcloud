from dash import html, dcc
import dash_bootstrap_components as dbc

from maps import map_region, map_basin, control_data_sel, control_time_sel
from plots import popup_plots
from tools import basin_tools

panel_layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([html.Div(map_region)]),
            dbc.Row([
                dbc.Col(html.Div(control_data_sel), width=6),
                dbc.Col(html.Div(control_time_sel), width=6),
            ], class_name='g-2', style={'padding-top': '3px'})
        ], width=7),
        dbc.Col([
            dbc.Row([html.Div([map_basin, popup_plots])]),
            dbc.Row([html.Div(basin_tools)], class_name='g-2', style={'padding-top': '3px'}),
        ], width=5),
    ], class_name='g-1'),
], style={'width': '95%', 'min-width': '1200px', 'min-height': '850px', 'margin-left': 'auto', 'margin-right': 'auto', 'margin-bottom': '170px', 'background': '#888888', 'padding': '3px'}) #1e6b8b

