from flask import Flask, render_template, redirect, request, url_for, flash
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
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
login = LoginManager(app)


class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    species = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return 'Pet %r' % self.id
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_admin(self):
        self.admin = True

    def __repr__(self):
        return 'User %r ' % self.username


##Forms
class petForm(FlaskForm):
    name= StringField('Enter a new name')
    species = StringField('Enter a new species')
    submit = SubmitField('Submit new pet')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')




##Paths
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)

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
            new_pet = Pets(species=species, age=age, filename=filename,name=name)
            try:
                db.session.add(new_pet)
                db.session.commit()
                return redirect(url_for('petlist'))
            except:
                print(species)
                print(name)
                print(filename)
                return "error"
    pets = Pets.query.order_by(Pets.id)
    return redirect(url_for('index'))

@app.route('/petlist')
def petlist():
    pets = Pets.query.order_by(Pets.id)
    return render_template('petList.html', pets=pets)
    
@app.route('/petview', methods=['POST', 'GET'])
def viewpet():
    pet_id = request.args.get('id')
    pets = Pets.query.filter(Pets.id == pet_id)
    return render_template('petview.html', pet=pets[0])
