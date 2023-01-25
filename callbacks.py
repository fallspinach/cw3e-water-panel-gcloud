from main import app
from config import all_stations, fnf_stations
from site_tools import draw_reana, draw_mofor, draw_table, draw_table_all
from basin_tools import draw_precip_by_elev

from dash.dependencies import ClientsideFunction, Input, Output, State

## Callbacks from here on

# callback to update data var in the title section
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_title_var'
    ),
    Output('title-var', 'children'),
    Input(component_id='data-sel',  component_property='value'),
    Input(component_id='met-vars',  component_property='value'),
    Input(component_id='hydro-vars', component_property='value')
)

# callback to update data date in the title section
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_title_date'
    ),
    Output('title-date', 'children'),
    Input('datepicker', 'date')
)

# callback to update url of image overlay
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_img_url'
    ),
    Output('data-img', 'url'),
    Input('datepicker', 'date'),
    Input(component_id='data-sel',  component_property='value'),
    Input(component_id='met-vars',  component_property='value'),
    Input(component_id='hydro-vars', component_property='value')
)

# callback to update url of color bar
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_cbar'
    ),
    Output('data-cbar-img', 'src'),
    Input(component_id='data-sel',  component_property='value'),
    Input(component_id='met-vars',  component_property='value'),
    Input(component_id='hydro-vars', component_property='value')
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_cbar_visibility'
    ),
    Output('data-cbar', 'style'),
    Input(component_id='data-map-ol', component_property='checked')
)

# callback to update datepicker and slider on button clicks
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_date'
    ),
    Output('datepicker', 'date'),
    Input('button-forward-day',  'n_clicks_timestamp'),
    Input('button-backward-day', 'n_clicks_timestamp'),
    Input('button-forward-month',   'n_clicks_timestamp'),
    Input('button-backward-month',  'n_clicks_timestamp'),
    Input('datepicker', 'date'),
    Input('datepicker', 'min_date_allowed'),
    Input('datepicker', 'max_date_allowed')
)

# create/update historic time series graph in popup
@app.callback(Output(component_id='graph-reana', component_property='figure'),
              Output(component_id='graph-mofor', component_property='figure'),
              Output(component_id='div-table', component_property='children'),
              Output('popup-plots', 'is_open'),
              Output('popup-plots', 'title'),
              Input('b120-points', 'click_feature'),
              Input('button-open-popup', 'n_clicks'))
def update_flows(fcst_point, n_clicks):
    if fcst_point==None:
        staid = 'FTO'
        stain = 'FTO: Feather River at Oroville'
    else:
        staid = fcst_point['properties']['Station_ID']
        stain = fcst_point['properties']['tooltip']
    fig_reana = draw_reana(staid)
    fig_mofor = draw_mofor(staid)
    if staid!='SRS':
        table_fcst = draw_table(staid, all_stations[staid])
    else:
        table_fcst = draw_table_all()
    
    return [fig_reana, fig_mofor, table_fcst, True, stain]

# callback to update basin tools
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_basin_elev'
    ),
    Output('elev-bands', 'url'),
    Input('b120-watersheds', 'click_feature')
)

# create/update precip by elev graph in basin tools
@app.callback(Output(component_id='graph-precip-by-elev', component_property='figure'),
              Input('b120-watersheds', 'click_feature'))
def update_precip_by_elev(basin):
    if basin==None:
        staid = 'FTO'
    else:
        staid = basin['properties']['Station']

    fig_precip_by_elev = draw_precip_by_elev(staid)
    
    return fig_precip_by_elev



