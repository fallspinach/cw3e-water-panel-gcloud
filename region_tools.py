from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import Namespace, arrow_function

from datetime import date, datetime, timedelta

from config import map_tiles, data_vars, obs_networks, basin_groups, df_system_status

# temporary set up
#curr_day   = (datetime.utcnow()-timedelta(days=1, hours=13)).date()
last_whmoni = datetime.fromisoformat(df_system_status['WRF-Hydro Monitor'][1]).date()
data_start = date(2021, 7, 1)

# start to build maps
ns = Namespace('dashExtensions', 'default')
locator = dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}})

# B-120 forecast points
b120_points = dl.GeoJSON(url='assets/fnf_points_proj_tooltip_24.pbf', format='geobuf', id='b120-points',
                         options=dict(pointToLayer=ns('b120_ptl')), cluster=True, superClusterOptions=dict(radius=5),
                         hoverStyle=arrow_function(dict(weight=5, color='red', fillColor='red', dashArray='')),
                         hideout=dict(circleOptions=dict(fillOpacity=1, color='red', weight=2, radius=5), colorscale=['cyan'], colorProp='POINT_Y', min=0, max=100))
# B-120 watersheds
watershed_style = dict(weight=2, opacity=1, color='darkblue', fillOpacity=0)
b120_watersheds = dl.GeoJSON(url='assets/fnf_watershed_proj_tooltip_24.pbf', format='geobuf', id='b120-watersheds',
                             options=dict(style=ns('b120_style')),
                             hoverStyle=arrow_function(dict(weight=4, color='brown', dashArray='', fillOpacity=0)),
                             hideout=dict(colorscale=['darkblue'], classes=[0], style=watershed_style, colorProp='Area_SqMi'))
# CNRFC region boundary
cnrfc_style = dict(weight=4, opacity=1, color='gray', fillOpacity=0)
cnrfc_bound = dl.GeoJSON(url='assets/cnrfc_bd_degree_wgs84.pbf', format='geobuf', id='cnrfc-bound',
                         options=dict(style=ns('b120_style')),
                         hideout=dict(colorscale=['black'], classes=[0], style=cnrfc_style, colorProp='Area_SqMi'))
# NWM rivers with stream_order>3 and simplified geometry
river_style = dict(weight=1, opacity=1, color='green', fillOpacity=0)
nwm_rivers = dl.GeoJSON(url='assets/nwm_reaches_cnrfc_order4plus_0d001_single_matched.pbf', format='geobuf', id='nwm-rivers',
                        options=dict(style=ns('river_style')), zoomToBoundsOnClick=True,
                        hoverStyle=arrow_function(dict(weight=4, color='orange', dashArray='', fillOpacity=0)),
                        hideout=dict(colorscale=['black'], classes=[0], style=river_style, colorProp='feature_id'))

# image data overlay
data_var_selected = 0
cnrfc_domain = [[32, -125], [44, -113]]
img_url  = last_whmoni.strftime(data_vars[data_var_selected]['url'])
cbar_url = data_vars[data_var_selected]['cbar']
data_map = dl.ImageOverlay(id='data-img', url=img_url, bounds=cnrfc_domain, opacity=0.7)
# color bar
data_cbar = html.Div(html.Img(src=cbar_url, title='Color Bar', id='data-cbar-img'), id='data-cbar',
                   style={'position': 'absolute', 'left': '18px', 'top': '140px', 'z-index': '500'})

layers_region = [dl.Overlay([data_map, data_cbar], id='data-map-ol',  name='Data',   checked=True),
                 dl.Overlay(cnrfc_bound,      id='region-ol', name='Region', checked=True),
                 dl.Overlay(nwm_rivers,       id='rivers-ol', name='Rivers', checked=True),
                 dl.Overlay(b120_watersheds,  id='basins-ol', name='Basins', checked=True),
                 dl.Overlay(b120_points,      id='sites-ol',  name='Sites',  checked=True)]
                 
# region map on the left
map_region = dl.Map([map_tiles[1], locator, dl.LayersControl(layers_region)], id='map-region',
                    center=[38.2, -119], zoom=6,
                    style={'width': '100%', 'height': '100%', 'min-height': '650px', 'min-width': '700px', 'margin': '0px', 'display': 'block'})


# met variable tab
tab_style  = {'min-height': '162px', 'background-color': 'white', 'font-size': 'small'}
item_style = {'margin': '5px 10px 2px 10px'}
met_vars = [{'label': v['label'], 'value': v['name']} for v in data_vars if v['cat']=='met']
met_tab = html.Div(dcc.RadioItems(options=met_vars, value=met_vars[0]['value'], id='met-vars', inputStyle=item_style), style=tab_style)

# hydro variable tab
hydro_vars = [{'label': v['label'], 'value': v['name']} for v in data_vars if v['cat']=='hydro']
hydro_tab = html.Div(dcc.RadioItems(options=hydro_vars, value=hydro_vars[data_var_selected]['value'], id='hydro-vars', inputStyle=item_style), style=tab_style)

# site tab
site_vars = [{'label': s, 'value': s} for s in obs_networks]
site_tab  = html.Div(dcc.RadioItems(options=site_vars, value=site_vars[0]['value'], inputStyle=item_style), style=tab_style)

# basin tab
basin_vars = [{'label': s, 'value': s} for s in basin_groups]
basin_tab  = html.Div(dcc.RadioItems(options=basin_vars, value=basin_vars[0]['value'], inputStyle=item_style), style=tab_style)

# tabs for map layer selection
tabtitle_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
tabtitle_selected_style = tabtitle_style.copy()
tabtitle_selected_style.update ({'font-weight': 'bold'})

control_data_sel = html.Div(dcc.Tabs([
    dcc.Tab(met_tab,   label='Meteorology', value='met',   style=tabtitle_style, selected_style=tabtitle_selected_style),
    dcc.Tab(hydro_tab, label='Hydrology',   value='hydro', style=tabtitle_style, selected_style=tabtitle_selected_style),
    dcc.Tab(site_tab,  label='Sites',       value='site',  style=tabtitle_style, selected_style=tabtitle_selected_style),
    dcc.Tab(basin_tab, label='Basins',      value='basin', style=tabtitle_style, selected_style=tabtitle_selected_style),
], value='hydro', id='data-sel'))


## hour slider
hour_marks = {}
for i in range(24):
    hour_marks[i] = '%d' % i
hour_marks[0] = '0z'
    
slider_hour =  html.Div(
    dcc.Slider(
        id='slider-hour',
        min=0,
        max=23,
        step=1,
        marks=hour_marks,
        value=0,
        disabled=True,
    ),
    id='slider-hour-container',
    style={'padding-top': '10px'}
)

datepicker = dcc.DatePickerSingle(
    id='datepicker',
    display_format='YYYY-MM-DD',
    min_date_allowed=data_start,
    max_date_allowed=last_whmoni,
    initial_visible_month=data_start,
    date=last_whmoni,
    day_size=30,
)

## buttons for forward and backward moves
button_style = {'margin': '0px 2px 0px 2px'}
button_backward_hour  = html.Button('<H', id='button-backward-hour',  n_clicks=0, style=button_style, disabled=True)
button_backward_day   = html.Button('<D', id='button-backward-day',   n_clicks=0, style=button_style)
button_backward_month = html.Button('<M', id='button-backward-month', n_clicks=0, style=button_style)
button_forward_hour   = html.Button('H>', id='button-forward-hour',   n_clicks=0, style=button_style, disabled=True)
button_forward_day    = html.Button('D>', id='button-forward-day',    n_clicks=0, style=button_style)
button_forward_month  = html.Button('M>', id='button-forward-month',  n_clicks=0, style=button_style)

## figure title
title_var  = html.Div(data_vars[data_var_selected]['label'], id='title-var',
                      style={'position': 'absolute', 'left': '50px', 'top': '625px', 'z-index': '500', 'font-size': 'medium'})
title_date = html.Div(last_whmoni.strftime(' @ %Y-%m-%d '), id='title-date',
                      style={'position': 'absolute', 'left': '245px', 'top': '625px', 'z-index': '500', 'font-size': 'medium'})

title_zone = html.Div([title_var, title_date], id='title-zone')

button_open_popup  = html.Button('Open Time Series Window', id='button-open-popup',  n_clicks=0, style={'margin-top': '15px'})

tab_stylec = tab_style.copy()
tab_stylec.update({'text-align': 'center', 'padding-top': '15px'})
# time step selection tab
timestep_tab = html.Div([button_backward_month, button_backward_day, button_backward_hour, datepicker, 
                         button_forward_hour, button_forward_day, button_forward_month, slider_hour, button_open_popup, title_var, title_date], style=tab_stylec)

## month slider
month_marks = {}
for i in range(12):
    month_marks[i] = '%d' % (i+1)
month_marks = {0: 'Jan', 1: 'Feb', 2: 'Mar', 3: 'Apr', 4: 'May', 5: 'Jun', 6: 'Jul', 7: 'Aug', 8: 'Sep', 9: 'Oct', 10: 'Nov', 11: 'Dec'}
    
slider_month =  html.Div(
    dcc.Slider(
        id='slider-month',
        min=0,
        max=11,
        step=1,
        marks=month_marks,
        value=0,
        disabled=True,
    ),
    id='slider-month-container',
    style={'padding-top': '10px'}
)

# monthly climatology selection tab
clim_tab = html.Div(['Select Month', slider_month], style=tab_stylec)

# tabs for time step selection
control_time_sel = html.Div(dcc.Tabs([
    dcc.Tab(timestep_tab, label='Time Step',   value='timestep', style=tabtitle_style, selected_style=tabtitle_selected_style),
    dcc.Tab(clim_tab,     label='Climatology', value='clime',    style=tabtitle_style, selected_style=tabtitle_selected_style),
], value='timestep'))

