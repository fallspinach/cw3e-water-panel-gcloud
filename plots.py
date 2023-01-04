from dash import html, dcc
import dash_bootstrap_components as dbc

popup_plots = dbc.Offcanvas(
    html.P('All the time series plots, tables, etc. here.'),
    title="Plots", placement='top', is_open=True, scrollable=True,
    style={'opacity': '0.9', 'width': '90%', 'min-width': '1000px', 'min-height': '500px', 'margin-top': '150px', 'margin-left': 'auto', 'margin-right': 'auto'}
)
