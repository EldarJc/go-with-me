import re

from database.models import User
from flask_wtf import FlaskForm
from wtforms import (
    DateTimeField,
    FieldList,
    FormField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, ValidationError

from . import REQUIRED_MSG


class AddAttendee(FlaskForm):
    class Meta:
        csrf = False

    username = StringField("Username", validators=[DataRequired(message=REQUIRED_MSG)])
    role = SelectField(
        "Role", choices=[], validators=[DataRequired(message=REQUIRED_MSG)]
    )

    def validate_username(self, field) -> None:
        if User.query.filter_by(username=field.data).first() is None:
            raise ValidationError(f"User '{field.data}' does not exist.")


class AddLocation(FlaskForm):
    class Meta:
        csrf = False

    country = StringField("Country", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])


class CreateEventForm(FlaskForm):
    title = StringField("Name", validators=[DataRequired(message=REQUIRED_MSG)])
    description = TextAreaField("Description", validators=[Length(max=500)])
    start_date = DateTimeField(
        "Start Time", validators=[DataRequired(message=REQUIRED_MSG)]
    )
    end_date = DateTimeField(
        "End Time", validators=[DataRequired(message=REQUIRED_MSG)]
    )
    location = FormField(AddLocation)
    attendees = FieldList(FormField(AddAttendee))
    group = SelectMultipleField("Group", choices=[])
    tags = SelectMultipleField("Tags", choices=[])
    submit = SubmitField("Create Event")

    def validate_title(self, field) -> None:
        title = field.data
        if re.search(r"^[\W_]", title):
            raise ValidationError("Title cannot begin with that character.")
        elif re.search(r"[\W_]$", title):
            raise ValidationError("Title cannot end with that character.")

    def validate(self, *args, **kwargs) -> bool:
        is_valid = super(CreateEventForm, self).validate(*args, **kwargs)
        start_date, end_date = self.start_date.data, self.end_date.data
        if start_date and end_date and start_date > end_date:
            self.start_date.errors.append("Start date cannot be greater than end date.")
            is_valid = False
        return is_valid
