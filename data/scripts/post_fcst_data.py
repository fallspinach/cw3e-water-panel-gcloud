import os
import pandas as pd
from glob import glob
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# alphabetical order
fnf_stations = ['AMF', 'CSN', 'EFC', 'EWR', 'FTO', 'KGF', 'KRI', 'KWT', 'MKM', 'MRC', 'MSS', 'PSH', 'SBB', 'SCC', 'SDT', 'SIS', 'SJF', 'SNS', 'TLG', 'TNL', 'TRF', 'WFC', 'WWR', 'YRS']
# north to south order - DWR likes this better
fnf_stations = ['TNL', 'SDT', 'MSS', 'PSH', 'SIS', 'SBB', 'FTO', 'YRS', 'AMF', 'CSN', 'MKM', 'SNS', 'TLG', 'MRC', 'SJF', 'KGF', 'KWT', 'SCC', 'KRI', 'TRF', 'WFC', 'EFC', 'WWR', 'EWR']

base_dir = '../'

datcols = ['Exc50','Pav50','Exc90','Pav90','Exc10','Pav10','Avg']
allcols = ['Date'] + datcols + ['Basin']

#print(allcols)

#for fcst_type in ['esp_wwrf_cdfm', 'esp_wwrf_lstm']:
for fcst_type in ['esp_wwrf_cdfm']:
    
    fcsts = glob(f'{base_dir}/forecast/{fcst_type}_update*')
    fcsts.sort()
    
    df = pd.DataFrame(columns=allcols)
    
    for fcst in fcsts:
        
        dt_up = datetime.strptime(os.path.basename(fcst).split('_')[-1], 'update%Y%m%d')
        if dt_up.month==1:
            dt_2  = datetime(dt_up.year, 7, 31)
        else:
            dt_2  = datetime(dt_up.year, dt_up.month, 1) + relativedelta(months=6) - timedelta(days=1)
        
        for staid in fnf_stations:
            
            f = f'{fcst}/{staid}_{dt_up:%Y%m}01-{dt_2:%Y%m%d}.csv'
            
            if not os.path.isfile(f):
                print(f'{f} is not found.')
                continue
                
            data = pd.read_csv(f)
            data['Date'] = f'{dt_up:%Y-%m-%d}'
            data['Basin'] = staid
            
            df.loc[len(df)] = data[allcols].iloc[-1]
            
    #print(df)
    if fcst_type=='esp_wwrf_cdfm':
        fout = f'{base_dir}/forecast/Apr2Jul_{dt_up.year}_CDF.csv'
    else:
        fout = f'{base_dir}/forecast/Apr2Jul_{dt_up.year}_LSTM.csv'
        
    df.to_csv(fout, index=False)

    os.system(f'rsync -a {fout} cw3e@cw3e.ucsd.edu:htdocs/wrf_hydro/b-120/streamflow/')
