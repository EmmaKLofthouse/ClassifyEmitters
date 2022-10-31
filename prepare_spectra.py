""" 
Prepare spectra for classification

make_trim: create spectra trimmed around the line of interest

"""


def find_nearest_index(array, value):
    import numpy as np 

    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def make_trim(sightline,dwlmin,dwlmax):
    """
    create spectra trimmed around the line of interest
    
    Inputs:
    dwlmin: lower limit on wavelengths relative to central wavelength of source
                
    dwlmax: upper limit on wavelengths relative to central wavelength of source

         
    """
    from astropy.table import Table
    from astropy.io import fits
    import pandas as pd
    import numpy as np
    import os

    data_path = ('/madfs/data/dc-fuma1/MUSELLSDATA/' 
                + 'emitter_sources/{}/extracted/'.format(sightline) + '/')

    #open table which contains wavelength of the line
    table = Table.read(data_path + 'COMBINED_CUBE_bootvar_cubex_psfsub'
                       + '_bkgsub_select_SNR.fits')

    df = table.to_pandas()

    sourceidlist = df['id']
    wllist = df['lambda_geow']

    #loop over sources
    for sid in range(len(sourceidlist)):
        print(sid)
        sourceid = sourceidlist[sid]

        #read in spectrum
        spec = fits.open(data_path + 'objs/id{}/'.format(sourceid)
                         + 'spectrum.fits')
        flux    = spec[0].data
        fluxerr = spec[1].data
        wave    = spec[2].data

        #determine wavelength range to cut to
        source_wl = wllist[sid]
        minwl_index = find_nearest_index(wave,source_wl-dwlmin)
        maxwl_index = find_nearest_index(wave,source_wl+dwlmax)

        #trim spectrum
        flux_trim    = flux[minwl_index:maxwl_index]
        fluxerr_trim = fluxerr[minwl_index:maxwl_index]
        wave_trim    = wave[minwl_index:maxwl_index]

        #save trimmed spectrum
        hduflx = fits.PrimaryHDU(flux_trim,header=spec[0].header)
        hduerr  = fits.ImageHDU(fluxerr_trim) #associated errors
        hduwav  = fits.ImageHDU(wave_trim)    #wave
        hdulist = fits.HDUList([hduflx,hduerr,hduwav])
        filename = ('/madfs/data/pkmt75/ML/data/' + 
                   'trimmed_spectra/{}/'.format(sightline) + 
                   'spec_trim_id{}'.format(sourceid) + 
                   '_-{}A_+{}A.fits'.format(dwlmin,dwlmax))

        #if using python 3.2 or later:
        #   os.makedirs(os.path.dirname(filename), exist_ok=True)
        #else:
        if not os.path.exists(os.path.dirname(filename)):
            try:    
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        hdulist.writeto(filename, overwrite=True)


    return


sightline_list = ['J010619+004823']#, 'J012403+004432', 'J013340+040059', 
                  #'J013724-422417', 'J015741-010629', 'J020944+051713', 
                  #'J024401-013403', 'J033413-161205', 'J033900-013318', 
                  #'J094932+033531', 'J095852+120245', 'J102009+104002',
                  #'J111008+024458', 'J111113-080401', 'J120917+113830',
                  #'J123055-113909', 'J124957-015928', 'J133254+005250', 
                  #'J142438+225600', 'J162116-004251', 'J193957-100241', 
                  #'J200324-325145', 'J205344-354652', 'J221527-161133', 
                  #'J230301-093930', 'J231543+145606', 'J233446-090812',
                  #'J234913-371259']

# loop over each sightline and then each source
for sightline in sightline_list:
    print(sightline)

    make_trim(sightline,100,100)
            


        
    


    

