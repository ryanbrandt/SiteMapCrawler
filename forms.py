from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class DomainForm(FlaskForm):
    '''
    Simple Flask form to grab selected domain to crawl-- saves me some time writing HTML
    '''
    domain = StringField(label='Domain', validators=[DataRequired()], widget=TextArea())
    algorithm = SelectField(label='Crawling Algorithm', choices=[('df', 'Depth-First'), ('bf', 'Breadth-First')], default='Breadth-First', validators=[DataRequired()])
    max_depth = IntegerField(label='Max Depth (Optional)')
    submit = SubmitField('Generate Site Map')