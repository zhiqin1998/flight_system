import copy
import datetime
import os

import plotly
import plotly.graph_objs as go
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

    def shortest_route(self, src, dst):
        pass

    def plot_words_hist(self, word_dicts, combine=True):
        word_dict = self.news_processor.combine_dicts(word_dicts)
        if combine:
            c = sum(value == 1 for value in word_dict.values())
            if c > 0:
                word_dict = {k: v for k, v in word_dict.items() if v > 1}
                word_dict['others'] = c
        word, count = map(list, [word_dict.keys(), word_dict.values()])
        return go.Bar(x=word, y=count, text=count, hoverinfo='y', textposition='auto', opacity=0.6)

    def plot_all_cities_hist(self, path=os.path.join('..', 'res', 'html', 'tmp.html'), group='pos+stop+neg+neu'):
        traces = [self.plot_single_city(c, 'hist', group=group) for c, _ in self.city_list.items()]
        self.plot(traces, 'News Word Counts Summary Histogram', path, layout=go.Layout(barmode='group'))

    def plot_single_city(self, code, graph_type='pie', stop_dicts=None, pos_dicts=None, neg_dicts=None, neu_dicts=None,
                         domain=None, group='pos+stop+neg+neu'):
        groups = group.split('+')
        if domain is None:
            domain = dict(x=[0, 1], y=[0, 1])
        if stop_dicts is None and pos_dicts is None and neg_dicts is None and neu_dicts is None:
            stop_dicts, pos_dicts, neg_dicts, neu_dicts = self.city_list[code].stop_dicts, self.city_list[
                code].pos_dicts, self.city_list[code].neg_dicts, self.city_list[code].neu_dicts
        labels, values = [], []
        if 'stop' in groups:
            labels.append('Stop Words')
            values.append(self.news_processor.count_dicts(stop_dicts))
        if 'pos' in groups:
            labels.append('Positive Words')
            values.append(self.news_processor.count_dicts(pos_dicts))
        if 'neg' in groups:
            labels.append('Negative Words')
            values.append(self.news_processor.count_dicts(neg_dicts))
        if 'neu' in groups:
            labels.append('Neutral Words')
            values.append(self.news_processor.count_dicts(neu_dicts))
        trace = None
        if graph_type == 'pie':
            trace = go.Pie(labels=labels, values=values,
                           hoverinfo='name+label+percent', textinfo='value',
                           textfont=dict(size=20),
                           name=code,
                           domain=domain,
                           marker=dict(line=dict(color='#000000', width=2)))
        elif graph_type == 'hist':
            trace = go.Bar(x=labels, y=values, text=values, hoverinfo='y+name',
                           name=self.city_list[code].name.split(',')[-1],
                           textposition='auto', opacity=0.6)
        return trace

    def plot_all_cities_pies(self, path=os.path.join('..', 'res', 'html', 'tmp.html'), group='pos+stop+neg+neu'):
        traces = []
        annotations = []
        x_low, x_high, y_low, y_high, i = 0, 0.2, 0, 0.5, 0
        for c, v in self.city_list.items():
            traces.append(
                self.plot_single_city(c, graph_type='pie', group=group,
                                      domain=dict(x=[x_low + 0.02, x_high - 0.02], y=[y_low + 0.01, y_high - 0.01])))
            annotations.append(
                dict(xanchor='center', yanchor='bottom', text=v.name.split(',')[-1], x=(x_low + x_high) / 2,
                     y=y_high - 0.06, xref='paper', showarrow=False, font=dict(size=20)))
            i += 1
            x_low += 0.2
            x_high += 0.2
            if i == 5:
                x_low, x_high = 0, 0.2
                y_high += 0.5
                y_low += 0.5
        self.plot(traces, 'News Word Counts Summary Pie Chart', path, annotations)

    def plot(self, trace, title, path=os.path.join('..', 'res', 'html', 'tmp.html'), annotations=None, auto_open=False,
             layout=None):
        if annotations is None:
            annotations = []
        if layout is None:
            layout = go.Layout(title=title, annotations=annotations)
        else:
            layout.title = title
            layout.annotations = annotations
        fig = go.Figure(data=trace, layout=layout)
        plotly.offline.plot(fig, filename=path, auto_open=auto_open)


if __name__ == '__main__':
    t1 = datetime.datetime.now()
    flightsystem = FlightRecommendSystem(gmap_api_key='YOUR_API_KEY')
    flightsystem.print_cities()
    flightsystem.print_dist_mat()
    print('time taken: {}'.format(datetime.datetime.now() - t1))
    flightsystem.plot_cities()
    flightsystem.plot([flightsystem.plot_single_city('ATL')], 'Atlanta')
    flightsystem.plot([flightsystem.plot_words_hist(flightsystem.city_list['ATL'].pos_dicts)], 'Atlanta Positive Words',
                      auto_open=True)
    flightsystem.plot_all_cities_hist(group='pos+neg+stop+neu')
    # flightsystem.plot_all_cities_pies()
