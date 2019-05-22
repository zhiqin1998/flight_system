from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField

from wtforms import validators, ValidationError


class ContactForm(Form):
    source = TextField("Source", [validators.Required("Enter the source")])
    destination = TextField("Destination", [validators.Required("Enter the destination")])
    submit = SubmitField("Send")