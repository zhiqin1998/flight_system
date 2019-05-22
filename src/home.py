from flask import Flask, render_template, request, flash
from src.forms import ContactForm
from src.main import FlightRecommendSystem
import datetime


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
            return render_template('success.html')
    elif request.method == 'GET':
        t1 = datetime.datetime.now()
        flightsystem = FlightRecommendSystem(gmap_api_key='AIzaSyDgNNtNRpti5pymuNaHy7vCIIL9sI5ruIA')
        flightsystem.print_cities()
        flightsystem.print_dist_mat()
        print('time taken: {}'.format(datetime.datetime.now() - t1))
        flightsystem.plot_cities()
        p = flightsystem.shortest_routes(source, 'ATL')
        p = flightsystem.sort_routes(p)
        [print(j) for j in p]
        flightsystem.plot_routes(p[:5])
        return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)