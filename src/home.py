from flask import Flask, render_template, request, flash
from src.forms import ContactForm

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
            return render_template('route.html')
    elif request.method == 'GET':
        return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)