from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask import redirect
from flask import request

app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    species = db.Column(db.String(200), nullable=False)
    picture = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return 'Pet %r' % self.id

class petForm(FlaskForm):
    name= StringField('Enter a new ingredient')
    species = StringField('Enter a new ingredient')
    picture = StringField('Enter a new ingredient')
    submit = SubmitField('Submit new pet')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    pet = None
    form = petForm()
    if form.validate_on_submit():
        species = form.species.data
        picture = form.picture.data
        name = form.name.data
        new_pet = Pets(species=species,picture=picture,name=name)
        try:
            db.session.add(new_pet)
            db.session.commit()
            return redirect('/')
        except:
            return "error"
        form.species.data = ''
        form.name.data = ''
        form.picture.data = ''
    pets = Pets.query.order_by(Pets.id)
    return render_template('index.html', form=form,pets=pets)
