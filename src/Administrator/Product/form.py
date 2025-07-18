
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField,DateField,ValidationError,FileField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp
from wtforms.widgets import TextArea
from src.Models.Category import Category
from src.db import db

def lodCategory():
    data = [('',"choose category")]
    QueryCategory = db.session.query(Category).all()

    for item in QueryCategory:
        data.append((item.id, item.name))

    return data

class ProductForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category_id.choices = lodCategory()

    name = StringField('Name' )
    # category_id = StringField('Category')
    price = StringField('Price', validators=[DataRequired(), Length(max=10)])
    qty = StringField('Quantity')
    date = DateField('Date')
    article = StringField('Article' )
    country = StringField('Country' )
    image = FileField('Image URL' )
    description = TextAreaField('Description')
    category_id = SelectField('Select Category', choices=[], coerce=str)

    # Submit button
    submit = SubmitField(
        'Save Customer',
        render_kw={"class": "btn btn-primary"}
    )

    def validate_price(self, field):
        try:
            float(field.data,)
        except (ValueError, TypeError):
            raise ValidationError('Price must be a (float).')