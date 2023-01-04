from dash import html, dcc
import dash_bootstrap_components as dbc

tab_style  = {'min-height': '412px', 'background-color': 'white', 'font-size': 'small'}
snow_tab = html.Div(['Basin Snowpack Analysis'], style=tab_style)


tab_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
tab_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

basin_tools = html.Div(dcc.Tabs([
    dcc.Tab([snow_tab], label='Snowpack',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(label='Soil Moisture',    style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(label='Tool X',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(label='Tool Y',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(label='Tool Z',  style=tab_style, selected_style=tab_selected_style),
]))

