from app import app
from flask import jsonify, request
import geopandas as gpd
import pandas as pd
from lcoe_model import lcoe_model

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

@app.route('/api/lcoe', methods=['POST'])
def lcoe_model_route():
    args=dict(
            size_kw              = request.json["size_kw"],
            esc                  = request.json["esc"],
            expected_yield_yr1   = request.json["yield_yr1"],
            lifespan             = request.json["lifespan"],
            degradation          = request.json["degredation"],
            soiling_yield_impact = request.json["soiling_yield_impact"],
            coating_yield_impact = request.json["coating_yield_impact"],
            coating_om_impact    = request.json["coating_om_impact"],
            coating_cost_per_m2  = request.json["coating_cost_per_m2"],
            coating_year         = request.json["coating_year"],
            module_watts         = request.json["module_watts"],
            module_area          = request.json["module_area"]
    )
    for k in args:
        args[k] = float(args[k])
    rv = lcoe_model(**args)
    return jsonify(rv)
