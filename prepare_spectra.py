""" 
Prepare spectra for classification

make_trim: create spectra trimmed around the line of interest

"""


def make_trim(spec):
    """
    create spectra trimmed around the line of interest
    """

    sightline_list = ['J010619+004823', 'J012403+004432', 'J013340+040059', 'J013724-422417', 'J015741-010629', 'J020944+051713', 'J024401-013403', 'J033413-161205', 'J033900-013318', 'J094932+033531', 'J095852+120245', 'J102009+104002', 'J111008+024458', 'J111113-080401', 'J120917+113830', 'J123055-113909', 'J124957-015928', 'J133254+005250', 'J142438+225600', 'J162116-004251', 'J193957-100241', 'J200324-325145', 'J205344-354652', 'J221527-161133', 'J230301-093930', 'J231543+145606', 'J233446-090812', 'J234913-371259']

    # loop over each sightline and then each source
    for sightline in sightline_list:

        #open table which contains wavelength of the line
        table = Table.read('/home/emma/Documents/laeML/data/catalogues/individual_cubes/{}_cubex_data.fits'.format(sightline))

        df = table.to_pandas()
	
        #loop over sources
	#grep idXX
	#sourceidlist = ... 
	for sourceid in sourceidlist
		spec = fits.open('/home/emma/Documents/laeML/data/{}/objs/{}/spectrum.fits'.format(sightline,sourceid))
	

	#determine wavelength range to cut to
	cen_wl = df['lambda_wl']

        
    


    

