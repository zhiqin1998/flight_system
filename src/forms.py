from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

from wtforms.validators import DataRequired


class RouteForm(FlaskForm):
    def validate(self):
        if self.source.data == 'None' or self.destination.data == 'None':
            return False
        return True
    source = SelectField('Sources', validators=[DataRequired()])
    destination = SelectField("Destination", validators=[DataRequired()])
    submit = SubmitField("Send")
