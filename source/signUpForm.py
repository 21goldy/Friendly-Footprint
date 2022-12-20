from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL


class LoginForm(FlaskForm):
    userName = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class ContactUsForm(FlaskForm):
    userName = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about = StringField("About", validators=[DataRequired()])
    submit = SubmitField("Submit")
