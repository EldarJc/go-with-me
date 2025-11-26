import re

from database.models import User
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from . import REQUIRED_MSG


class SignUpForm(FlaskForm):

    first_name = StringField(
        "First Name", validators=[DataRequired(message=REQUIRED_MSG)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(message=REQUIRED_MSG)]
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message=REQUIRED_MSG),
            Email(message="Invalid email address format."),
        ],
    )
    username = StringField(
        "Username",
        validators=[
            DataRequired(message=REQUIRED_MSG),
            Length(max=50, message="Username cannot be longer than 50 characters."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message=REQUIRED_MSG),
            Length(min=8, message="Password must have a minimum of 8 characters."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(message=REQUIRED_MSG)]
    )
    submit = SubmitField("Sign Up")

    def validate_email(self, field) -> None:
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("This email address is not available")

    def validate_username(self, field) -> None:
        username = field.data
        if re.search(r"^[\W_]", username):
            raise ValidationError("Username cannot begin with that character.")

        elif re.search(r"[\W_]$", username):
            raise ValidationError("Username cannot end with that character")

        elif User.query.filter_by(username=username).first():
            raise ValidationError("This username is not available")

    def validate(self, *args, **kwargs) -> bool:
        is_valid = super(SignUpForm, self).validate(*args, **kwargs)
        password, confirm_password = self.password.data, self.confirm_password.data
        if confirm_password != password:
            self.confirm_password.errors.append("Passwords do not match.")
            is_valid = False
        return is_valid
