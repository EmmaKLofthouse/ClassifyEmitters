



import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

# Read in individual datacubes and combine into a single dataframe

from astropy.table import Table
import pandas as pd

df = pd.DataFrame()

sightline_list = ['J010619+004823','J012403+004432','J013340+040059']


#['J010619+004823']#,'J012403+004432','J013340+040059','J013724-422417','J015741-010629']#,
                  #'J020944+051713','J024401-013403','J033413-161205','J033900-013318','J094932+033531',
                 #'J095852+120245']#,'J102009+104002','J111008+024458','J111113-080401','J120917+113830',
                  #'J123055-113909','J124957-015928','J133254+005250','J142438+225600','J162116-004251',
                  #'J193957-100241','J200324-325145','J205344-354652','J221527-161133','J230301-093930',
                  #'J231543+145606','J233446-090812','J234913-371259']


for sightline in sightline_list:
    table = Table.read('/home/emma/Documents/laeML/data/catalogues/individual_cubes/{}_cubex_data.fits'.format(sightline))
    table['sightline'] = sightline
    pandas_df = table.to_pandas()
    df = pd.concat([df,pandas_df])

# Cut to SNR > 7 as we haven't looked at all the sources below this
df = df[df.SNR >= 7]

# Check number of LAEs
type_str = df['type'].str.decode("utf-8")
nLAE = type_str.str.contains('LAE').sum()
#print(nLAE)


# Create new column to show if entry is an LAE
df['isLAE'] = np.where(type_str.str.contains('LAE'), 1, 0)


y=df.isLAE


#create empty list
#xlist = []
#open existing dataframe
xlist = []

with open(r"../data/trimmed_spectra_dataframe.txt", 'r') as fp:
    for line in fp:
        x = line[:-1]

        # add current item to the list
        xlist.append(x)


#print(xlist)
from astropy.io import fits

#loop over entries, find the trimmed spectrum, add to dataframe
for row in df.itertuples(index=True, name='Pandas'):
    trimmed_file = '/home/emma/Documents/laeML/data/trimmed_spec/{}/spec_trim_id{}_-100A_+100A.fits'.format(row.sightline,row.id)
    
    #read in spectrum
    try:
        with fits.open(trimmed_file) as spec:
            flx = spec[0].data
            xlist.append(flx)
    except:
        print('Couldn\'t find: ' +str(row.sightline) + ' id' + str(row.id))
        continue
        
    
with open("../data/trimmed_spectra_dataframe.txt", 'w') as fp:
    for item in xlist:
        # write each item on a new line
        fp.write("%s\n" % item)


#x=pd.DataFrame(xlist)
#x.head()


