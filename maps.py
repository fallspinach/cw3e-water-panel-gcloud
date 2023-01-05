from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import Namespace, arrow_function

from datetime import date, datetime, timedelta


# temporary set up
curr_day   = (datetime.utcnow()-timedelta(days=1, hours=14)).date()
#curr_day   = date(2022, 12, 31)
data_start = date(2021, 7, 1)
data_end   = curr_day

## data variables
monitor_url = 'https://cw3e.ucsd.edu/wrf_hydro/cnrfc/imgs/monitor/'
data_vars = [{'label': 'SWE Percentile (daily)',    'name': 'swe_r',    'cat': 'hydro', 'url': monitor_url+'output/%Y/swe_r_%Y%m%d.png',   'cbar': monitor_url+'output/swe_r_cbar.png'},
             {'label': '2-m SM Percentile (daily)', 'name': 'smtot_r',  'cat': 'hydro', 'url': monitor_url+'output/%Y/smtot_r_%Y%m%d.png', 'cbar': monitor_url+'output/smtot_r_cbar.png'},
             {'label': 'Precipitation (daily)',     'name': 'precip',   'cat': 'met',   'url': monitor_url+'forcing/%Y/precip_%Y%m%d.png', 'cbar': monitor_url+'forcing/precip_cbar.png'},
             {'label': 'Air Temperature (daily)',   'name': 'tair2m',   'cat': 'met',   'url': monitor_url+'forcing/%Y/tair2m_%Y%m%d.png', 'cbar': monitor_url+'forcing/tair2m_cbar.png'},
             {'label': 'P Percentile (monthly)',    'name': 'precip_r', 'cat': 'met',   'url': monitor_url+'forcing/%Y/precip_r_%Y%m.png', 'cbar': monitor_url+'forcing/precip_r_cbar.png'},
             {'label': 'T Percentile (monthly)',    'name': 'tair2m_r', 'cat': 'met',   'url': monitor_url+'forcing/%Y/atir2m_r_%Y%m.png', 'cbar': monitor_url+'forcing/tair2m_r_cbar.png'}]

# start to build maps
ns = Namespace('dashExtensions', 'default')
locator = dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}})

# some available map tiles
maptiles = [
    dl.TileLayer(url='https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png',
        #attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, <a href="https://openmaptiles.org/">OpenMapTiles</a>, <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
    ),
    dl.TileLayer(url='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.png',
        #attribution='<a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    ),
    dl.TileLayer(url='http://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
        #attribution='&copy; Esri and Community'
    )
]

# B-120 forecast points
b120_points = dl.GeoJSON(url='assets/fnf_points_proj_tooltip.pbf', format='geobuf', id='b120-points',
                         options=dict(pointToLayer=ns('b120_ptl')), cluster=True, superClusterOptions=dict(radius=5),
                         hoverStyle=arrow_function(dict(weight=5, color='red', fillColor='red', dashArray='')),
                         hideout=dict(circleOptions=dict(fillOpacity=1, color='red', weight=2, radius=5), colorscale=['cyan'], colorProp='POINT_Y', min=0, max=100))
# B-120 watersheds
watershed_style = dict(weight=2, opacity=1, color='darkblue', fillOpacity=0)
b120_watersheds = dl.GeoJSON(url='assets/fnf_watershed_proj_tooltip.pbf', format='geobuf', id='b120-watersheds',
                             options=dict(style=ns('b120_style')),
                             hoverStyle=arrow_function(dict(weight=4, color='brown', dashArray='', fillOpacity=0)),
                             hideout=dict(colorscale=['darkblue'], classes=[0], style=watershed_style, colorProp='Area_SqMi'))
# CNRFC region boundary
cnrfc_style = dict(weight=4, opacity=1, color='gray', fillOpacity=0)
cnrfc_bound = dl.GeoJSON(url='assets/cnrfc_bd_degree_wgs84.pbf', format='geobuf', id='cnrfc-bound',
                         options=dict(style=ns('b120_style')),
                         hideout=dict(colorscale=['black'], classes=[0], style=cnrfc_style, colorProp='Area_SqMi'))

# image data overlay
data_var_selected = 1
cnrfc_domain = [[32, -125], [44, -113]]
img_url  = curr_day.strftime(data_vars[data_var_selected]['url'])
cbar_url = data_vars[data_var_selected]['cbar']
data_map = dl.ImageOverlay(id='data-img', url=img_url, bounds=cnrfc_domain, opacity=0.7)
# color bar
data_cbar = html.A(html.Img(src=cbar_url, title='Color Bar', id='data-cbar-img'), id='data-cbar',
                   style={'position': 'absolute', 'left': '18px', 'top': '140px', 'z-index': '500'})

layers_region = [dl.Overlay([data_map, data_cbar], id='data-map-ol',  name='Data',   checked=True),
                 dl.Overlay(cnrfc_bound,      id='region-ol', name='Region', checked=True),
                 dl.Overlay(b120_watersheds,  id='basins-ol', name='Basins', checked=True),
                 dl.Overlay(b120_points,      id='sites-ol',  name='Sites',  checked=True)]
                 
# region map on the left
map_region = dl.Map([maptiles[1], locator, dl.LayersControl(layers_region)],
                    center=[38.2, -119], zoom=6,
                    style={'width': '100%', 'height': '100%', 'min-height': '650px', 'min-width': '700px', 'margin': '0px', 'display': 'block'})

# B-120 basin elevation bands
#elev_scale = ['green', 'lightgreen', 'lightyellow', 'yellow', 'darkyellow', 'brown', 'darkbrown', 'darkred', 'darkgray', 'gray', 'lightgray', 'white']
elev_scale = ['magenta', 'red', 'orangered', 'orange', 'yellow', 'yellowgreen', 'green', 'cyan', 'turquoise', 'blue', 'indigo', 'purple', 'violet']
elev_classes = [-1, 999, 1999, 2999, 3999, 4999, 5999, 6999, 7999, 8999, 9999, 10999]
elev_style = dict(weight=0, opacity=1, color='darkblue', fillOpacity=0.3)
elev_bands = dl.GeoJSON(url='assets/elev_bands_FTO.pbf', format='geobuf', id='elev-bands', zoomToBounds=True,
                        options=dict(style=ns('b120_style')),
                        hoverStyle=arrow_function(dict(weight=1, color='black', dashArray='', fillOpacity=0.5)),
                        hideout=dict(colorscale=elev_scale, classes=elev_classes, style=elev_style, colorProp='low_range'))
                        
# basin zoom-in map on the right
map_basin  = dl.Map([maptiles[2], elev_bands],
                    center=[40, -121], zoom=8, zoomControl=False,
                    style={'width': '100%', 'height': '100%', 'min-height': '400px', 'min-width': '500px', 'margin': '0px', 'display': 'block'})


# met variable tab
tab_style  = {'min-height': '162px', 'background-color': 'white', 'font-size': 'small'}
item_style = {'margin': '5px 10px 2px 10px'}
met_vars = [{'label': v['label'], 'value': v['name']} for v in data_vars if v['cat']=='met']
met_tab = html.Div(dcc.RadioItems(options=met_vars, value=met_vars[0]['value'], id='met-vars', inputStyle=item_style), style=tab_style)

# hydro variable tab
hydro_vars = [{'label': v['label'], 'value': v['name']} for v in data_vars if v['cat']=='hydro']
hydro_tab = html.Div(dcc.RadioItems(options=hydro_vars, value=hydro_vars[data_var_selected]['value'], id='hydro-vars', inputStyle=item_style), style=tab_style)

# site tab
site_vars = [{'label': s, 'value': s} for s in ['Bulletin 120', 'USGS', 'CW3E']]
site_tab  = html.Div(dcc.RadioItems(options=site_vars, value=site_vars[0]['value'], inputStyle=item_style), style=tab_style)

# basin tab
basin_vars = [{'label': s, 'value': s} for s in ['Bulletin 120', 'HUC-8', 'HUC-10', 'HUC-12']]
basin_tab  = html.Div(dcc.RadioItems(options=basin_vars, value=basin_vars[0]['value'], inputStyle=item_style), style=tab_style)

# tabs for map layer selection
tabtitle_style          = {'padding': '2px', 'height': '28px', 'font-size': 'small'}
tabtitle_selected_style = {'padding': '2px', 'height': '28px', 'font-size': 'small', 'font-weight': 'bold'}

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
    max_date_allowed=data_end,
    initial_visible_month=data_start,
    date=curr_day,
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
title_date = html.Div(curr_day.strftime(' @ %Y-%m-%d '), id='title-date',
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

