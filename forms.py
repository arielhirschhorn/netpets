from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, HiddenField, SelectField
from wtforms.validators import DataRequired, URL, Optional, NumberRange
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed

class addPet(FlaskForm):
    pet_name = StringField('Name:', validators=[DataRequired()])
    pet_picture = FileField('Picture:', validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    pet_species = SelectField('Species:', choices=[('cat', 'cat'), ('dog', 'dog'), ('fish', 'fish'), ('other', 'other')], 
    submit = SubmitField('Add it!')
