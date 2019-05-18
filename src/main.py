import datetime
import os
import copy

from gmplot import *

from src.city import City
from src.geolib import GeoLib
from src.news_processor import NewsProcessor


class FlightRecommendSystem:
    def __init__(self, gmap_api_key, code_ref=os.path.join('..', 'res', 'airport code references.txt')):
        self.gmap_api_key = gmap_api_key
        self.geolib = GeoLib(gmap_api_key)
        self.news_processor = NewsProcessor()
        self.code_ref_path = code_ref
        self.city_list = None
        self.dist_mat = None
        self.init_city_list()
        self.update_city_coord()
        self.gen_dist_mat()
        self.process_all_news()
        min_lat, max_lat, min_lon, max_lon = min([c.coor[0] for _, c in self.city_list.items()]), max(
            [c.coor[0] for _, c in self.city_list.items()]), min([c.coor[1] for _, c in self.city_list.items()]), max(
            [c.coor[1] for _, c in self.city_list.items()])
        self.base_gmap = gmplot.GoogleMapPlotter((min_lat + max_lat) / 2, (min_lon + max_lon) / 2, 3)
        self.base_gmap.apikey = self.gmap_api_key
        self.base_gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

    def plot_cities(self, file_path=os.path.join('..', 'res', 'html', 'cities.html')):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        tmp = copy.deepcopy(self.base_gmap)
        [tmp.marker(c.coor[0], c.coor[1], title=c.name) for _, c in self.city_list.items()]
        tmp.draw(file_path)

    def process_all_news(self):
        self.news_processor.process_all(self.city_list)

    def update_city_coord(self):
        self.geolib.update_all_coordinate(self.city_list)

    def gen_dist_mat(self):
        self.dist_mat = self.geolib.gen_distance_matrix(self.city_list)

    def init_city_list(self):
        self.city_list = dict(
            (line.split(':')[0].strip(), City(line.split(':')[0].strip(), line.split(':')[1].strip())) for line in
            open(self.code_ref_path, 'r').read().strip().split('\n'))

    def print_cities(self):
        [print(v) for _, v in self.city_list.items()]

    def print_dist_mat(self):
        self.geolib.print_dist_mat(self.dist_mat)


if __name__ == '__main__':
    t1 = datetime.datetime.now()
    flightsystem = FlightRecommendSystem(gmap_api_key='YOUR_API_KEY')
    flightsystem.print_cities()
    flightsystem.print_dist_mat()
    print('time taken: {}'.format(datetime.datetime.now() - t1))
    flightsystem.plot_cities()
