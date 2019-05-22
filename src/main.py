import copy
import datetime
import functools
import os

import plotly
import plotly.graph_objs as go
from flask import Flask, render_template, request, flash
from gmplot import *

from src.city import City
from src.forms import ContactForm
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
        self.color = ['red', 'blue', 'orange', 'white', 'purple', 'yellow', 'pink', 'green']
        min_lat, max_lat, min_lon, max_lon = min([c.coor[0] for _, c in self.city_list.items()]), max(
            [c.coor[0] for _, c in self.city_list.items()]), min([c.coor[1] for _, c in self.city_list.items()]), max(
            [c.coor[1] for _, c in self.city_list.items()])
        self.base_gmap = self.create_gmap((min_lat + max_lat) / 2, (min_lon + max_lon) / 2)

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

    def shortest_routes(self, src, dst, min_max=(2, 3)):
        min, max = min_max
        p, ans = [src], []

        def cust_bfs(path, dist, pol):
            if len(path) <= max + 2:
                cur = path[-1]
                if cur == dst:
                    if len(path) >= min + 2:
                        ans.append((path, dist, pol))
                else:
                    [cust_bfs(path + [c], dist + self.dist_mat[cur][c], pol + self.city_list[c].pol_senti) for c in
                     sorted(self.city_list, key=lambda k: self.dist_mat[cur][k]) if c != cur and c != src]

        cust_bfs(p, 0, 0)
        return ans

    def sort_routes(self, routes, range_threshold=1000):
        def cmp(a, b):
            # if abs(a[1] - b[1]) < range_threshold:
            if int(a[1] / range_threshold) == int(b[1] / range_threshold):
                return b[2] - a[2]
            else:
                return a[1] - b[1]

        return sorted(routes, key=functools.cmp_to_key(cmp))

    def create_gmap(self, lat, lon, zoom=3):
        base_gmap = gmplot.GoogleMapPlotter(lat, lon, zoom)
        base_gmap.apikey = self.gmap_api_key
        base_gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
        return base_gmap

    def plot_routes(self, routes, gmap=None, file_path=os.path.join('..', 'src', 'templates', 'route.html'),
                    plot_src_dst=True):
        src, dst = routes[0][0][0], routes[0][0][-1]
        mid_lat, mid_lon = (self.city_list[src].coor[0] + self.city_list[dst].coor[0]) / 2, (
                self.city_list[src].coor[1] + self.city_list[dst].coor[1]) / 2
        if (abs(self.city_list[src].coor[1] - self.city_list[dst].coor[1])) > 180:
            mid_lon += 180.0
        if gmap is None:
            gmap = self.create_gmap(mid_lat, mid_lon, 2)
        for i in range(len(routes)):
            latitude_list, longitude_list = map(list, zip(*[self.city_list[c].coor for c in routes[i][0]]))
            gmap.plot(latitude_list, longitude_list, self.color[i], edge_width=len(routes) - i)
        if plot_src_dst:
            gmap.plot([self.city_list[src].coor[0], self.city_list[dst].coor[0]],
                      [self.city_list[src].coor[1], self.city_list[dst].coor[1]], color='black', edge_width=2.5)
        gmap.draw(file_path)

    def plot_words_hist(self, word_dicts, combine=True):
        word_dict = self.news_processor.combine_dicts(word_dicts)
        if combine:
            c = sum(value == 1 for value in word_dict.values())
            if c > 0:
                word_dict = {k: v for k, v in word_dict.items() if v > 1}
                word_dict['others'] = c
        word, count = map(list, [word_dict.keys(), word_dict.values()])
        return go.Bar(x=word, y=count, text=count, hoverinfo='y', textposition='auto', opacity=0.6)

    def plot_all_cities_hist(self, path=os.path.join('..', 'src', 'templates', 'cityhist.html'),
                             group='pos+stop+neg+neu'):
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

    def plot_all_cities_pies(self, path=os.path.join('..', 'src', 'templates', 'citypies.html'),
                             group='pos+stop+neg+neu'):
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

    def plot(self, trace, title, path, annotations=None, auto_open=False,
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


app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/form', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('form.html', form=form)
        else:
            p = flightsystem.shortest_routes(form.source._value(), form.destination._value())
            p = flightsystem.sort_routes(p)
            [print(j) for j in p]
            flightsystem.plot_routes(p[:5])
            flightsystem.plot(
                [flightsystem.plot_single_city(form.destination._value(), group='pos+neg+neu+stop', graph_type='hist')],
                form.destination._value(), path=os.path.join('..', 'src', 'templates', 'singlecity.html'))
            flightsystem.plot(
                [flightsystem.plot_words_hist(flightsystem.city_list[form.destination._value()].pos_dicts)],
                'Positive Words',
                path=os.path.join('..', 'src', 'templates', 'singlehist.html'))
            flightsystem.plot_all_cities_hist(group='pos+neg+stop+neu')
            flightsystem.plot_all_cities_pies()

            return render_template('dashboard.html')
    elif request.method == 'GET':
        return render_template('form.html', form=form)


# @app.route('/<string:page_name>/')
# def render_static(page_name):
#     if not page_name.endswith('.html'):
#         page_name = '{}.html'.format(page_name)
#     return render_template('{}'.format(page_name))
@app.route('/cityhist', methods=['GET', 'POST'])
def cityhist():
    return render_template('cityhist.html')


@app.route('/citypies', methods=['GET', 'POST'])
def citypies():
    return render_template('citypies.html')


@app.route('/singlecity', methods=['GET', 'POST'])
def singlecity():
    return render_template('singlecity.html')


@app.route('/singlehist', methods=['GET', 'POST'])
def singlehist():
    return render_template('singlehist.html')


@app.route('/routes', methods=['GET', 'POST'])
def route():
    return render_template('route.html')


if __name__ == '__main__':
    t1 = datetime.datetime.now()
    flightsystem = FlightRecommendSystem(gmap_api_key='AIzaSyDgNNtNRpti5pymuNaHy7vCIIL9sI5ruIA')
    flightsystem.print_cities()
    flightsystem.print_dist_mat()
    print('time taken: {}'.format(datetime.datetime.now() - t1))
    flightsystem.plot_cities()
    app.run(debug=True)

    # flightsystem.plot([flightsystem.plot_single_city('ATL', group='pos+neg+neu+stop', graph_type='hist')], 'Atlanta')
    # flightsystem.plot([flightsystem.plot_words_hist(flightsystem.city_list['ATL'].pos_dicts)],
    #                   'Atlanta Positive Words', auto_open=True)
    # flightsystem.plot_all_cities_hist(group='pos+neg+stop+neu')
    # flightsystem.plot_all_cities_pies()
