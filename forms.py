from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class AddTask(FlaskForm):
    controller = StringField('Controller', validators=[DataRequired()])
    target = StringField('Target', validators=[DataRequired()])
    action = StringField('Action', validators=[DataRequired()])

class AddUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

class AddDevice(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
