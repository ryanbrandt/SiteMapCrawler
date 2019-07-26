from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class DomainForm(FlaskForm):
    '''
    Simple Flask form to grab selected domain to crawl-- saves me some time writing HTML
    '''
    domain = StringField(label='Your Domain', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Generate Site Map')