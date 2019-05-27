from flask_wtf import Form
from wtforms import SubmitField, SelectField, StringField

from wtforms.validators import DataRequired


class ContactForm(Form):
    def validate(self):
        if self.source.data == 'None' or self.destination.data == 'None':
            return False
        return True

    source = SelectField('Sources', validators=[DataRequired()])
    destination = SelectField("Destination", validators=[DataRequired()])
    sortby = SelectField("Sort By", validators=[DataRequired()])
    groups = StringField("Group Range", validators=[DataRequired()], default="1000")
    submit = SubmitField("Send")
