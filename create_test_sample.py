"""
Create an initial small sample of X true LAEs and X noise

"""

from astropy.table import Table
from astropy.io import fits
import pandas as pd
import numpy as np
import os

sightline_list = ['J010619+004823', 'J012403+004432', 'J013340+040059',
                  'J013724-422417', 'J015741-010629', 'J020944+051713', 
                  'J024401-013403', 'J033413-161205', 'J033900-013318', 
                  'J094932+033531', 'J095852+120245', 'J102009+104002',
                  'J111008+024458', 'J111113-080401', 'J120917+113830',
                  'J123055-113909', 'J124957-015928', 'J133254+005250', 
                  'J142438+225600', 'J162116-004251', 'J193957-100241', 
                  'J200324-325145', 'J205344-354652', 'J221527-161133', 
                  'J230301-093930', 'J231543+145606', 'J233446-090812',
                  'J234913-371259']

# loop over each sightline and then each source
for sightline in sightline_list:
    print(sightline)
    
    data_path = ('/madfs/data/dc-fuma1/MUSELLSDATA/' 
                + 'emitter_sources/{}/extracted/'.format(sightline) + '/')

    #open table which contains wavelength of the line
    table = Table.read(data_path + 'COMBINED_CUBE_bootvar_cubex_psfsub'
                       + '_bkgsub_select_SNR.fits')

    df = table.to_pandas()
    df['sightline'] = sightline

    LAEs = df[df.type =='LAE']
    Junk = df[df.type =='None']

    if sightline == sightline_list[0]:
    #create master dataframe of LAEs and junk
        AllLAEs = LAEs
        AllJunk = Junk
    else:
        AllLAEs = pd.concat([AllLAEs,LAEs])
        AllJunk = pd.concat([AllJunk,Junk])
    

#Select sample at random
nrows = 1000
LAESample = AllLAEs.sample(nrows)
JunkSample = AllJunk.sample(nrows)

LAESample.to_csv('../data/LAESample'+str(nrows)+'.csv',index=False)
LAESample.to_csv('../data/JunkSample'+str(nrows)+'.csv',index=False)








