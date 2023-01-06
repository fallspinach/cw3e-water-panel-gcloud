from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import Namespace, arrow_function

from region_tools import maptiles

# start to build maps
ns = Namespace('dashExtensions', 'default')

# B-120 basin elevation bands
elev_scale = ['magenta', 'red', 'orangered', 'orange', 'yellow', 'yellowgreen', 'green', 'cyan', 'turquoise', 'blue', 'indigo', 'purple', 'violet']
elev_classes = [-1, 999, 1999, 2999, 3999, 4999, 5999, 6999, 7999, 8999, 9999, 10999, 11999]
elev_style = dict(weight=0, opacity=1, color='darkblue', fillOpacity=0.3)
elev_bands = dl.GeoJSON(url='assets/elev_bands_FTO.pbf', format='geobuf', id='elev-bands', zoomToBounds=True,
                        options=dict(style=ns('b120_style')),
                        hoverStyle=arrow_function(dict(weight=1, color='black', dashArray='', fillOpacity=0.5)),
                        hideout=dict(colorscale=elev_scale, classes=elev_classes, style=elev_style, colorProp='low_range'))
                        
# basin zoom-in map on the right
map_basin  = dl.Map([maptiles[2], elev_bands],
                    center=[40, -121], zoom=8, zoomControl=False,
                    style={'width': '100%', 'height': '100%', 'min-height': '400px', 'min-width': '500px', 'margin': '0px', 'display': 'block'})


tool_style  = {'min-height': '412px', 'background-color': 'white', 'font-size': 'small'}
precip_by_elev_tab = html.Div(['Precipitation across elevation bands.'], style=tool_style)
snow_tab           = html.Div(['Snowpack and rain-on-snow risk analysis.'], style=tool_style)


tab_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
tab_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

basin_tools = html.Div(dcc.Tabs([
    dcc.Tab([precip_by_elev_tab], label='Precipitation',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab([snow_tab],           label='Snowpack',       style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder 1'], style=tool_style), label='Soil Moisture',    style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder X'], style=tool_style), label='Tool X',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder Y'], style=tool_style), label='Tool Y',  style=tab_style, selected_style=tab_selected_style),
    dcc.Tab(html.Div(['Placeholder Z'], style=tool_style), label='Tool Z',  style=tab_style, selected_style=tab_selected_style),
]))

