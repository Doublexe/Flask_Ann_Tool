from flask_wtf import FlaskForm
from wtforms import (StringField,IntegerField, SubmitField, DateField, BooleanField,
                     TextAreaField,BooleanField, SelectField, SelectMultipleField)
from wtforms.validators import DataRequired, Optional, ValidationError, Email


class RecordSelectForm(FlaskForm):
    Record = SelectField(label='Record', choices=None, validators=[Optional()])

    def __init__(self, record_list):
        super(RecordSelectForm, self).__init__()
        RecordSelectForm.Record = SelectField(label='Record', choices=record_list, validators=[Optional()])
