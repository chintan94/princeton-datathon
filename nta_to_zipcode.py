import numpy as np
import pandas as pd

path = '../Datathon_Materials/' # change as needed
df_geo = pd.read_csv(path + 'geographic.csv')
df_demo = pd.read_csv(path + 'demographics_city.csv')

# find and store coordinates of NTAs
nta_coordinates = {}
for c in df_geo.columns:
	lon = df_geo[c][::2]
	lat = df_geo[c][1::2]
	x = 0.5*(max(lon)+min(lon))
	y = 0.5*(max(lat)+min(lat))
	nta_coordinates[c] = [x, y]

# append coordinates to demographic info
for i in range(len(df_demo)):
	nta = df_demo.iloc[i,2]
	x, y = nta_coordinates[nta]
	df_demo.loc[df_demo.index[i], 'longitude'] = x
	df_demo.loc[df_demo.index[i], 'latitude'] = y

# get zipcode-coordinate pairs from 311 dataset
df_311 = pd.read_csv(path + '311_service_requests.csv')
zip2location = df_311[['incident_zip', 'latitude', 'longitude']]
zip2location = zip2location.dropna()
zip2location = zip2location[zip2location['incident_zip']>1e4]
zip2location = zip2location[zip2location['incident_zip']<2e4]


zips = np.array(zip2location['incident_zip'])
lons = np.array(zip2location['longitude'])
lats = np.array(zip2location['latitude'])

keys = df_demo.columns[3:-2]
unique_zips = list(set(zips))
demo_by_zip = pd.DataFrame(index = unique_zips)
for k in keys:
    demo_by_zip[k] = [0.]*len(unique_zips)
demo_by_zip['nta_per_zip'] = [0.]*len(unique_zips)

for i in range(len(df_demo)):
    lon = df_demo.loc[i, 'longitude']
    lat = df_demo.loc[i, 'latitude']
    print df_demo.loc[i, 'nta_code'], lon, lat,
    distances = np.sqrt(np.cos(lat)**2*(lon-lons)**2 + (lat-lats)**2)
    ind = np.argmin(distances)
    this_zip = zips[ind]
    R = 6.3*1e3 # radius of the earth in km, to convert angle to distance
    print this_zip, R*distances[ind], 
    if R*distances[ind]>20:
        print "km is too far"
        this_zip = np.nan # undetermined
    else:
        print "km is ok"
        for key in demo_by_zip.columns:
            if key=='nta_per_zip':
                demo_by_zip.loc[this_zip, key] += 1
            else:
                demo_by_zip.loc[this_zip, key] += df_demo.loc[i, key]

demo_by_zip = demo_by_zip[demo_by_zip['nta_per_zip']>0] #at least one NTA falls under given zip
for z in demo_by_zip.index: # normalize mean/median values
	ct = demo_by_zip.loc[z, 'nta_per_zip']
	demo_by_zip.loc[z, 'median_income'] /= ct 
	demo_by_zip.loc[z, 'mean_income'] /= ct
	demo_by_zip.loc[z, 'people_per_acre'] /= ct
	demo_by_zip.loc[z, 'median_age'] /= ct

print demo_by_zip

demo_by_zip.to_csv('demographics_by_zipcode.csv')
