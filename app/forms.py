from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    photo = FileField('Photo',validators=[FileRequired(),FileAllowed(['jpg','png'])])
    description = StringField('Description', validators=[DataRequired()])