from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp
from wtforms.widgets import TextArea

class EmployeeForm(FlaskForm):

    name = TextAreaField('Name')

    # Submit button
    submit = SubmitField(
        'Save Employee',
        render_kw={"class": "btn btn-primary"}
    )