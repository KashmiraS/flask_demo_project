from wtforms import StringField, SubmitField, TextAreaField, DateField
from flask_wtf import FlaskForm


class AddProject(FlaskForm):
    project_name = StringField('Project Name ')
    project_description = TextAreaField('Enter Descriptions of project in short ')
    project_starting_date = DateField('Starting date ', id='start_date')
    project_releasing = DateField('Releasing date ', id='releasing_date')

    customer_name = StringField('Name ')
    customer_contact = StringField('Contact No. ')
    customer_mail = StringField('mail Id ')
    customer_company_name = StringField('Company Name ')
    customer_site = StringField('Company url ')
    # is software company future entity
    submit = SubmitField('Create')
    submit_save = SubmitField('Save')


class ShareProjectForm(FlaskForm):
    mail_id = StringField('Please use registered user id for sharing project')
    submit = SubmitField('share')
