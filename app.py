from flask import Flask, render_template, jsonify
import geopandas as gpd
import json

app = Flask(__name__)

gdf = gpd.read_feather('data/final/final_sal.feather').to_crs(epsg=4326)

# Convert gdf to GeoJSON
def gdf_to_geojson(gdf, properties):
    gdf['features'] = gdf.apply(lambda row: {
        'type': 'Feature',
        'geometry': json.loads(row['geometry'].to_json()),
        'properties': {prop: row[prop] for prop in properties}
    }, axis=1)
    return json.dumps({
        'type': 'FeatureCollection',
        'features': list(gdf['features'])
    })

@app.route('/')
def index():
    return render_template('index.html', amenity_type=['restaurant', 'cafe', 'school'],
                           stat_type=['within 2km', 'within 1km', 'within 500m', 'within 200m', 'closest'])

@app.route('/data/<amenity>/<stat>')
def data(amenity, stat):
    col_name = f'{amenity} - {stat}'
    properties = [col_name] 
    geojson_data = gdf_to_geojson(gdf, properties)
    return jsonify(geojson_data)

if __name__ == '__main__':
    app.run(debug=True)
