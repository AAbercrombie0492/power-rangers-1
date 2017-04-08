from app import app
from flask import jsonify, request
import geopandas as gpd
import pandas as pd

@app.route('/api/regions/shapes')
def query_region_shapes():
    """ Get region shapes as a geojson """
    region_df = gpd.read_file("app/data/shapes.geojson")
    return region_df.to_json()

@app.route('/api/regions/data/<list:columns>')
def query_region_data(columns):
    region_df = pd.read_csv("app/data/region_info.csv")
    region_df = region_df[columns]
    return region_df.T.to_json()
