from flaskext.wtf import Form, ValidationError, TextField, PasswordField, required, email as email_validator

from api.models import User


class LoginForm(Form):

    username = TextField("Username", validators=[
                         required(message="Username required")])

    password = PasswordField("Password", validators=[
                             required(message="Password required")])


class SignupForm(Form):

    username = TextField("Username", validators=[
                         required(message="Username required")])

    password = PasswordField("Password", validators=[
                             required(message="Password required")])

    email = TextField("Email address", validators=[
                      required(message="Email address required"),
                      email_validator(message="A valid email address is required")])

    def validate_username(self, field):
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError, "This username is taken"

    def validate_email(self, field):
        user = User.query.filter(User.email.like(field.data)).first()
        if user:
            raise ValidationError, "This email is taken"
