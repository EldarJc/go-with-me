import re

from database.models import Group
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from . import REQUIRED_MSG


class CreateGroupForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            DataRequired(message=REQUIRED_MSG),
            Length(max=100, message="Name cannot be longer than 100 characters."),
        ],
    )
    description = StringField("Description", validators=[Length(max=500)])
    tags = SelectMultipleField("Tags", choices=[])
    submit = SubmitField("Create Group")

    def validate_name(self, field) -> None:
        name = field.data
        if re.search(r"^[\W_]", name):
            raise ValidationError("Name cannot begin with that character.")
        elif re.search(r"[\W_]$", name):
            raise ValidationError("Name cannot end with that character.")
        elif Group.query.filter_by(name=name).first():
            raise ValidationError("This group name is not available")
