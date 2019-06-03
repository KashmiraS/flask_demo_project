from wtforms import StringField, SubmitField, RadioField, SelectField,TextAreaField,DateField
from flask_wtf import FlaskForm


class add_project(FlaskForm):
    project_name = StringField('Project Name ')
    project_description = TextAreaField('Enter Descriptions of project in short ')
    #project_language = StringField('Project Language')
    project_starting_date = DateField('Starting date ', id='start_date')
    project_releasing = DateField('Releasing date ', id='releasing_date')

    customer_name = StringField('Name ')
    customer_contact = StringField('Contact No. ')
    customer_mail = StringField('mail Id ')
    customer_company_name = StringField('Company Name ')
    customer_site = StringField('Company url ')
    # is software company
    submit = SubmitField('Create')