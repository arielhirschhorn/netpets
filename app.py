from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import os



app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config["IMAGE_UPLOADS"] = 'static/uploads'


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
    # picture = FileField('Upload image')
    submit = SubmitField('Submit new pet')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    #I'm sure there's a more efficient way to do it than loading the entire list 
    #and then trimming it, but I just needed to get something working so I could work on styling it
    pets = Pets.query.order_by(Pets.id)
    previews = pets[:4]
    return render_template('index.html', previews=previews)
    
@app.route('/addPet')
def petList():
    return render_template('addPet.html')


@app.route('/addPet', methods=['POST', 'GET'])
def upload_file():
    pet = None
    uploaded_file = request.files['file']
    if request.method == "POST":
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config["IMAGE_UPLOADS"], uploaded_file.filename))
            species = request.form['species']
            name = request.form['petname']
            filename = uploaded_file.filename
            new_pet = Pets(species=species, filename=filename,name=name)
            try:
                db.session.add(new_pet)
                db.session.commit()
                return redirect(url_for('petlist'))
            except:
                print(species)
                print(name)
                print(filename)
                return "error"
        # form.species.data = ''
        # form.name.data = ''
        # form.filename.data = ''
    pets = Pets.query.order_by(Pets.id)
    return redirect(url_for('index'))


# def submit():
#     pet = None
#     form = petForm()
#     if form.validate_on_submit():
#         species = form.species.data
#         picture = picture.save(form.picture.data)
#         filename = picture.url(filename)
#         saved_picture.save(os.path.join(app.config['UPLOAD_PATH'], picture)) 
#         name = form.name.data
#         new_pet = Pets(species=species, filename=filename,name=name)
#         try:
#             db.session.add(new_pet)
#             db.session.commit()
#             return redirect('/petlist')
#         except:
#             return "error"
#         form.species.data = ''
#         form.name.data = ''
#         form.picture.data = ''
#     pets = Pets.query.order_by(Pets.id)
#     return render_template('addPet.html', form=form,pets=pets)


@app.route('/petlist')
def petlist():
    pets = Pets.query.order_by(Pets.id)
    return render_template('petList.html', pets=pets)
    
@app.route('/petview')
def viewpet():
    pet_id = request.args.get('id')
    pets = Pets.query.filter(Pets.id == pet_id)
    return render_template('petview.html', pet=pets[0])
