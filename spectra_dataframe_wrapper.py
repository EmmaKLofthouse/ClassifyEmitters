
def runSpectraDataframe(sl):
    """
    create list of fluxes for all sources
    """
    import os
    import subprocess
    import sys


    #next prepare the script for the job
    scr=open("spectra_list_{}.py".format(sl),"w")
    
    scr.write("import pandas as pd \n")
    scr.write("import sys \n")
    scr.write("from astropy.table import Table\n")
    scr.write("sl=sys.argv[1] \n")
    scr.write("table = Table.read('/home/emma/Documents/laeML/data/catalogues/individual_cubes/{}_cubex_data.fits'.format(sl))\n")
    scr.write("table['sightline'] = sl\n")
    scr.write("df = table.to_pandas()\n")

    scr.write("df = df[df.SNR >= 7]\n")

    scr.write("import pickle\n")
    scr.write("try:\n")
    scr.write("    with open ('trimmed_spectra_pickle.txt', 'rb') as fp:\n")
    scr.write("        xlist = pickle.load(fp)\n")
    scr.write("except:\n")
    scr.write("    xlist=[]\n")

    scr.write("from astropy.io import fits\n")

    scr.write("for row in df.itertuples(index=True, name='Pandas'):\n")
    scr.write("    trimmed_file = '/home/emma/Documents/laeML/data/trimmed_spec/{}/spec_trim_id{}_-100A_+100A.fits'.format(row.sightline,row.id)\n")
        
    scr.write("    try:\n")
    scr.write("        with fits.open(trimmed_file) as spec:\n")
    scr.write("            flx = spec[0].data\n")
    scr.write("            xlist.append(flx)\n")
    scr.write("    except:\n")
    scr.write("        print('Couldnt find: ' +str(row.sightline) + ' id' + str(row.id))\n")
    scr.write("        continue\n")
            
    scr.write("with open('trimmed_spectra_pickle.txt', 'wb') as fp:\n")
    scr.write("    pickle.dump(xlist, fp)\n")
    scr.write("print(sys.argv[1])")
    scr.close()

    #schedule the job for execution
    subprocess.call("python spectra_list_{}.py {} \n".format(sl,sl), shell=True)

    return


sightline_list = ['J010619+004823', 'J012403+004432', 'J013340+040059', 'J013724-422417',
                  'J015741-010629', 'J020944+051713', 'J024401-013403', 'J033413-161205',
                  'J033900-013318', 'J094932+033531', 'J095852+120245']

for sl in sightline_list:
    runSpectraDataframe(sl)


#unpickle data
import pickle
import pandas as pd

with open ('trimmed_spectra_pickle.txt', 'rb') as fp:
    pickledata = pickle.load(fp)

df_pickle = pd.DataFrame(pickledata)
df_pickle.to_csv("trimmed_spectra_dataframe.csv")


