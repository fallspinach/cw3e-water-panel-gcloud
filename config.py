#### Configuration data here

import dash_leaflet as dl
import pandas as pd
from glob import glob
from datetime import datetime

###############################
## global configs

# system status
base_url = 'https://cw3e.ucsd.edu/wrf_hydro/cnrfc/' # easier to update the data but slow to load
fcsv = base_url + 'imgs/monitor/system_status.csv'
df_system_status = pd.read_csv(fcsv, parse_dates=True)

# temporary fix for possible inconsistency between gcloud and system files
fcstfiles = glob('data/monitor/CHRTOUT_????????-????????.daily.db')
fcstfiles.sort()
lastfcst = fcstfiles[-1].split('/')[-1].split('.')[0].split('_')[-1]
df_system_status['WWRF Forecast'][0]  = datetime.strptime(lastfcst.split('-')[0], '%Y%m%d').isoformat();
df_system_status['WWRF Forecast'][1]  = datetime.strptime(lastfcst.split('-')[1], '%Y%m%d').isoformat();

# image snapshot export options
graph_config = {'toImageButtonOptions': {'format': 'svg', 'filename': 'cw3e_water_panel_plot'}} 

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
          
obs_networks = ['Bulletin 120', 'DWR/CDEC', 'CNRFC', 'CW3E', 'SNOTEL', 'USGS', 'MADIS']
basin_groups = ['Bulletin 120', 'CNRFC', 'FIRO', 'HUC-8', 'HUC-10', 'HUC-12']
   
###############################
## site tools section

all_stations = {'AMF': 'American River below Folsom Lake', 'ASP': 'Arroyo Seco near Pasadena', 'ASS': 'Arroyo Seco near Soledad', 'CSN': 'Cosumnes River at Michigan Bar', 'EFC': 'East Carson near Gardnerville', 'EWR': 'East Walker near Bridgeport', 'ERS': 'Eel River at Scotia', 'FTO': 'Feather River at Oroville', 'KWT': 'Kaweah River below Terminus reservoir', 'KRB': 'Kern River below City of Bakersfield', 'KRI': 'Kern River below Lake Isabella', 'KGF': 'Kings River below Pine Flat reservoir', 'KLO': 'Klamath River Copco to Orleans', 'MSS': 'McCloud River above Shasta Lake', 'MRC': 'Merced River below Merced Falls', 'MKM': 'Mokelumne River inflow to Pardee', 'NCD': 'Nacimiento below Nacimiento Dam', 'NPH': 'Napa River near St Helena', 'OWL': 'Owens River below Long Valley Dam', 'PSH': 'Pit River near Montgomerey and Squaw Creek', 'RRH': 'Russian River at Healdsburg', 'SBB': 'Sacramento R above Bend Bridge', 'SDT': 'Sacramento River at Delta', 'SRS': 'Salmon River at Somes Bar', 'SJF': 'San Joaquin River below Millerton Lake', 'ANM': 'Santa Ana River near Mentone', 'SSP': 'Sespe Creek near Fillmore', 'SIS': 'Shasta Lake Total Inflow', 'SNS': 'Stanislaus River below Goodwin', 'TNL': 'Trinity River near Lewiston Lake', 'TRF': 'Truckee River from Tahoe to Farad', 'SCC': 'Tule River below Lake Success', 'TLG': 'Tuolumne River below Lagrange reservoir', 'WFC': 'West Fork Carson at Woodfords', 'WWR': 'West Walker near Coleville', 'YRS': 'Yuba River near Smartsville'}

# alphabetical order
fnf_stations = ['AMF', 'CSN', 'EFC', 'EWR', 'FTO', 'KGF', 'KRI', 'KWT', 'MKM', 'MRC', 'MSS', 'PSH', 'SBB', 'SCC', 'SDT', 'SIS', 'SJF', 'SNS', 'TLG', 'TNL', 'TRF', 'WFC', 'WWR', 'YRS']
# north to south order - DWR likes this better
fnf_stations = ['TNL', 'SDT', 'MSS', 'PSH', 'SIS', 'SBB', 'FTO', 'YRS', 'AMF', 'CSN', 'MKM', 'SNS', 'TLG', 'MRC', 'SJF', 'KGF', 'KWT', 'SCC', 'KRI', 'TRF', 'WFC', 'EFC', 'WWR', 'EWR']

fnf_id_names = {key: all_stations[key] for key in fnf_stations}


###############################
## basin tools section

