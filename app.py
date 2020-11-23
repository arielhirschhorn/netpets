from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, HiddenField, FileField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask import redirect
from flask import request



app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    species = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return 'Pet %r' % self.id

class petForm(FlaskForm):
    name= StringField('Enter a new name')
    species = StringField('Enter a new species')
    picture = FileField('Upload image')
    submit = SubmitField('Submit new pet')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def submit():
    pet = None
    form = petForm()
    if form.validate_on_submit():
        species = form.species.data
        picture = picture.save(form.picture.data)
        filename = picture.url(filename)
        saved_picture.save(os.path.join(app.config['UPLOAD_PATH'], picture)) 
        name = form.name.data
        new_pet = Pets(species=species, filename=filename,name=name)
        try:
            db.session.add(new_pet)
            db.session.commit()
            return redirect('/petlist')
        except:
            return "error"
        form.species.data = ''
        form.name.data = ''
        form.picture.data = ''
    pets = Pets.query.order_by(Pets.id)
    return render_template('addPet.html', form=form,pets=pets)


@app.route('/petlist', methods=['GET', 'POST'])
def petlist():
    pets = Pets.query.order_by(Pets.id)
    return render_template('index.html', pets=pets)
