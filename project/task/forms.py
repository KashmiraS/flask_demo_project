from wtforms import StringField, SubmitField,TextAreaField,DateField
from flask_wtf import FlaskForm

class create_task_form(FlaskForm):
    title = StringField('Task title')
    details = TextAreaField('Details')
    start_date = DateField('Start date',id='start_date')
    end_date = DateField('End date',id='enddate')
    submit = SubmitField('Create')
