from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField,FileField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp
from wtforms.widgets import TextArea

class SliderForm(FlaskForm):

    name = StringField('Name')
    image=FileField('Image')

    # Submit button
    submit = SubmitField(
        'Save Customer',
        render_kw={"class": "btn btn-primary"}
    )