import os

import googlemaps
from geopy.distance import great_circle

from src.city import City


class GeoLib:
    def __init__(self, gmap_api_key):
        self.gmap_api_jey = gmap_api_key
        self.geolocator = googlemaps.Client(key=gmap_api_key)

    def get_coordinate(self, name):
        geocode_result = self.geolocator.geocode(name)
        # print(name, location.latitude, location.longitude)
        return geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']

    def update_all_coordinate(self, city_ref):
        for k, v in city_ref.items():
            v.coor = self.get_coordinate(v.name)
        return city_ref

    def get_distance(self, city1, city2, city_ref):
        return float(great_circle(city_ref[city1].coor, city_ref[city2].coor).kilometers)

    def gen_distance_matrix(self, city_ref):
        d = {}
        for code1 in city_ref.keys():
            d[code1] = {}
            for code2 in city_ref.keys():
                d[code1][code2] = self.get_distance(code1, code2, city_ref)
        return d

    def print_dist_mat(self, dist_mat):
        [print(city1, city2, d) for city1, v in dist_mat.items() for city2, d in v.items()]


if __name__ == '__main__':
    geolib = GeoLib('AIzaSyDgNNtNRpti5pymuNaHy7vCIIL9sI5ruIA')
    ref_code = os.path.join('..', 'res', 'airport code references.txt')
    city_ref = dict(
        (line.split(':')[0].strip(), City(line.split(':')[0].strip(), line.split(':')[1].strip())) for line in
        open(ref_code, 'r').read().strip().split('\n'))
    print(city_ref)
    geolib.update_all_coordinate(city_ref)
    print(city_ref)
    dist_mat = geolib.gen_distance_matrix(city_ref)
    geolib.print_dist_mat(dist_mat)
