import requests
import pandas as pd
from shapely.geometry import Point

def get_data_from_api(base_url, params, save_file=False, dry=False):
    unwrapped_params = {
        key: ','.join(map(str, value)) if isinstance(value, list) else value
        for key, value in params.items()
    }

    if dry:
        req = requests.Request('GET', base_url, params=unwrapped_params)
        prepared_req = req.prepare()
        return prepared_req.url

    response = requests.get(base_url, params=unwrapped_params)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    data = response.json()

    if save_file:
        with open(save_file, 'w') as file:
            json.dump(data, file)


    return data


def create_point_geometry(coord):
    if 'lat' in coord and 'lng' in coord:
        return Point(coord['lng'], coord['lat'])
    else:
        raise ValueError("Dictionary must contain 'lat' and 'lng' keys.")