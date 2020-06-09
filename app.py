from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "tuesday-fun"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    """Redirect to register."""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def user_register():
    """User register form  """

    form = RegisterForm()

    if form.validate_on_submit():
        form_values = {
            'username': form.username.data,
            'password': form.password.data,
            'email': form.email.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data
        }

        if User.query.filter_by(username=form_values['username']).count() == 0:
            user = User.register(**form_values)
            db.session.add(user)
            db.session.commit()
            return redirect('/secret')

    return render_template('register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            # could save whole user in session if we want
            session["user_id"] = user.id  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.route("/secret")
def secret():
    """Example hidden page for logged-in users only."""

    if "user_id" not in session:
        return redirect("/login")
    else:
        return render_template("secret.html")

@app.route("/logout")
def log_out():
    """Log out a user """

    session.pop("user_id")

    return redirect("/")

@app.route("/users/<string:username>")
def show_user_page(username):
    """Show a user's profile"""

    if "user_id" not in session:
        return redirect("/login")

    else:
        user = User.query.filter(User.username == username).first()
        if user.username == username:
            return render_template("user.html", user=user)
    
        return redirect("/users/<string:username>")