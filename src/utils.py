
import pandas as pd
from shapely.geometry import Point


def create_point_geometry(coord):
    if 'lat' in coord and 'lng' in coord:
        return Point(coord['lng'], coord['lat'])
    else:
        raise ValueError("Dictionary must contain 'lat' and 'lng' keys.")