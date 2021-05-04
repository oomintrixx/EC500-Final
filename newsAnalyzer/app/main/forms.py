from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    query = StringField('keyword', validators=[DataRequired()])
    submit = SubmitField('Search')

class NewsForm(FlaskForm):
    keyword = StringField('keyword', validators=[DataRequired()])
    submit = SubmitField('Submit')
