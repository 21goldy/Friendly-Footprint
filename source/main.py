import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, url_for, flash
from flask_login import UserMixin, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from signUpForm import LoginForm, ContactUsForm

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CONFIGURE TABLE
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Contact(UserMixin, db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    about = db.Column(db.String(256))


db.create_all()


@app.route('/', methods=["GET", "POST"])
def index():
    form = ContactUsForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            return redirect(url_for('index'))

        new_contact = Contact(
            email=form.email.data,
            name=form.userName.data,
            about=form.about.data,
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("index.html", form=form)


@app.route('/shop')
def shop():
    return render_template("shop.html")


@app.route('/signUp', methods=["GET", "POST"])
def signUp():
    form = LoginForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('index'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.userName.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("index"))

    return render_template("sign_up.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
