from dash import html, dcc
import dash_bootstrap_components as dbc

tool_style  = {'min-height': '412px', 'background-color': 'white', 'font-size': 'small'}
snow_tab = html.Div(['Placeholder 1'], style=tool_style)


tab_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
tab_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

basin_tools = html.Div(dcc.Tabs([
    dcc.Tab([snow_tab], label='Snowpack',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder 2'], style=tool_style), label='Soil Moisture',    style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder 3'], style=tool_style), label='Tool X',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder 4'], style=tool_style), label='Tool Y',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder 5'], style=tool_style), label='Tool Z',  style=tab_style, selected_style=tab_selected_style),
]))

