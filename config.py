#### Configuration data here

import dash_leaflet as dl

###############################
## region tools section

# some available map tiles
map_tiles = [
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

## data variables
base_url = 'https://cw3e.ucsd.edu/wrf_hydro/cnrfc/imgs/'
data_vars = [
    {'label': 'SWE Percentile (daily)',    'name': 'swe_r',    'cat': 'hydro', 'url': base_url+'monitor/output/%Y/swe_r_%Y%m%d.png',   'cbar': base_url+'monitor/output/swe_r_cbar.png'},
    {'label': '2-m SM Percentile (daily)', 'name': 'smtot_r',  'cat': 'hydro', 'url': base_url+'monitor/output/%Y/smtot_r_%Y%m%d.png', 'cbar': base_url+'monitor/output/smtot_r_cbar.png'},
    {'label': 'Precipitation (daily)',     'name': 'precip',   'cat': 'met',   'url': base_url+'monitor/forcing/%Y/precip_%Y%m%d.png', 'cbar': base_url+'monitor/forcing/precip_cbar.png'},
    {'label': 'Air Temperature (daily)',   'name': 'tair2m',   'cat': 'met',   'url': base_url+'monitor/forcing/%Y/tair2m_%Y%m%d.png', 'cbar': base_url+'monitor/forcing/tair2m_cbar.png'},
    {'label': 'P Percentile (monthly)',    'name': 'precip_r', 'cat': 'met',   'url': base_url+'monitor/forcing/%Y/precip_r_%Y%m.png', 'cbar': base_url+'monitor/forcing/precip_r_cbar.png'},
    {'label': 'T Percentile (monthly)',    'name': 'tair2m_r', 'cat': 'met',   'url': base_url+'monitor/forcing/%Y/atir2m_r_%Y%m.png', 'cbar': base_url+'monitor/forcing/tair2m_r_cbar.png'},
    {'label': 'MODIS Snow Cover',          'name': 'modis_sca','cat': 'hydro', 'url': base_url+'obs/modis/%Y/modis_sca_%Y%m%d.png',    'cbar': base_url+'obs/modis/modis_sca_cbar.png'}
]
             
###############################
## site tools section

all_stations = {'AMF': 'American River below Folsom Lake', 'ASP': 'Arroyo Seco near Pasadena', 'ASS': 'Arroyo Seco near Soledad', 'CSN': 'Cosumnes River at Michigan Bar', 'EFC': 'East Carson near Gardnerville', 'EWR': 'East Walker near Bridgeport', 'ERS': 'Eel River at Scotia', 'FTO': 'Feather River at Oroville', 'KWT': 'Kaweah River below Terminus reservoir', 'KRB': 'Kern River below City of Bakersfield', 'KRI': 'Kern River below Lake Isabella', 'KGF': 'Kings River below Pine Flat reservoir', 'KLO': 'Klamath River Copco to Orleans', 'MSS': 'McCloud River above Shasta Lake', 'MRC': 'Merced River below Merced Falls', 'MKM': 'Mokelumne River inflow to Pardee', 'NCD': 'Nacimiento below Nacimiento Dam', 'NPH': 'Napa River near St Helena', 'OWL': 'Owens River below Long Valley Dam', 'PSH': 'Pit River near Montgomerey and Squaw Creek', 'RRH': 'Russian River at Healdsburg', 'SBB': 'Sacramento R above Bend Bridge', 'SDT': 'Sacramento River at Delta', 'SRS': 'Salmon River at Somes Bar', 'SJF': 'San Joaquin River below Millerton Lake', 'ANM': 'Santa Ana River near Mentone', 'SSP': 'Sespe Creek near Fillmore', 'SIS': 'Shasta Lake Total Inflow', 'SNS': 'Stanislaus River below Goodwin', 'TNL': 'Trinity River near Lewiston Lake', 'TRF': 'Truckee River from Tahoe to Farad', 'SCC': 'Tule River below Lake Success', 'TLG': 'Tuolumne River below Lagrange reservoir', 'WFC': 'West Fork Carson at Woodfords', 'WWR': 'West Walker near Coleville', 'YRS': 'Yuba River near Smartsville'}

fnf_stations = ['AMF', 'CSN', 'EFC', 'EWR', 'FTO', 'KGF', 'KRI', 'KWT', 'MKM', 'MRC', 'MSS', 'PSH', 'SBB', 'SCC', 'SDT', 'SIS', 'SJF', 'SNS', 'TLG', 'TNL', 'TRF', 'WFC', 'WWR', 'YRS']
fnf_stations = ['TNL', 'SDT', 'MSS', 'PSH', 'SIS', 'SBB', 'FTO', 'YRS', 'AMF', 'CSN', 'MKM', 'SNS', 'TLG', 'MRC', 'SJF', 'KGF', 'KWT', 'SCC', 'KRI', 'TRF', 'WFC', 'EFC', 'WWR', 'EWR']

fnf_id_names = {key: all_stations[key] for key in fnf_stations}


###############################
## basin tools section

