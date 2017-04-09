import geopandas as gpd
import mplleaflet
import shapely
import pandas as pd
import numpy as np
import seaborn as sns
import pysal as ps
from rasterstats import zonal_stats
import rasterio
import googlemaps
import re
from geopandas.tools import sjoin

import rasterio
import rasterio.features
import rasterio.warp
from rasterstats import zonal_stats

def get_climate_regions():
    with open('../data/KoeppenGeiger.UScounty.txt','rt') as f:
        climate_regions_raw = f.read()
        f.close()

        rows = climate_regions_raw.split('\n')
        climate_regions_table = [r.split('\t') for r in rows]

        # climate_regions_table[:10]
        columns = climate_regions_table[0]
        data = climate_regions_table[1:]

        climate_regions_df = pd.DataFrame(data, columns=columns)

        return climate_regions_df

def get_zipcodes():
    zips = gpd.read_file('../data/cb_2016_us_zcta510_500k/cb_2016_us_zcta510_500k.shp')
    return zips

def get_counties():
    counties = gpd.read_file('../data/cb_2016_us_county_5m/cb_2016_us_county_5m.shp')
    return counties

def county_pv_out():
    county_pv_stats = zonal_stats("../data/cb_2016_us_county_5m/cb_2016_us_county_5m.shp", "../data/PVOUT_USA.tif")
    county_pv_max = [z['max'] for z in county_pv_stats]
    return county_pv_stats

def split_geojson(geodf, name, nways=8):
    way_split= np.array_split(geodf, nways)
    for i, split in tqdm(enumerate(way_split)):
        split_fpath = '{}_pt{}.geojson'.format(name,i+1)
        with open(split_fpath, 'wt') as f:
            f.write(split.to_json())
            f.close()
        print(split_fpath)

def merge_counties_with_regions():
    counties_regions_soiling = pd.merge(counties,climate_regions_soiling,on='COUNTY', how='left')
    counties_regions_soiling_no_dupl = counties_regions_soiling.drop_duplicates('GEOID')

    def pct_to_number(row):
        slf_str = str(row)
        slf_fl = float(slf_str.strip('%'))
        return slf_fl

    counties_regions_soiling_no_dupl['MAX_DAILY_SLF_DECREASE'] = counties_regions_soiling['Max daily SLF decrease'].apply(lambda x: pct_to_number(x))
    return counties_regions_soiling_no_dupl

if __name__ == '__main__':
    climate_regions_soiling = get_climate_regions()
    # zips = get_zipcodes()
    # counties = get_counties()
    print('LOADING FILES')
    print('LOADING ZIP CLIMATE GEO')
    consolidated_zip_climate_geodf = gpd.read_file('../notebooks/zipcode_climate_county.geojson')
    print('LOADING ZIPCODES SHP')
    zipcodes_shp = gpd.read_file('../data/tl_2015_us_zcta510/tl_2015_us_zcta510.shp')
    print('LOADING COUNTIES SHP')
    counties = gpd.read_file('../data/cb_2016_us_county_5m/cb_2016_us_county_5m.shp')

    counties_regions_soiling_no_dupl = merge_counties_with_regions()
    with open('counties_regions_soiling.geojson', 'wt') as f:
        f.write(counties_regions_soiling_no_dupl)
        f.close()

    county_pv_stats = county_pv_out()
    county_pv_max = [c['max'] for c in county_pv_stats]
    counties_redux = counties[['COUNTY','geometry','max_PV']]
    counties_json = counties_redux.to_json()

    with open('counties_pv.geojson', 'wt') as f:
        f.write(counties_json)
        f.close()
