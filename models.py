from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.String(20),
                         unique=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    reviews = db.relationship('Feedback')

    @classmethod
    def register(cls, **kwargs):
        """Register user w/hashed password & return user."""
        # form_values = {key: value for key, value in kwargs.items()}

        hashed = bcrypt.generate_password_hash(kwargs['password'])
        # turn bytestring into normal (unicode utf8) string
        kwargs['password'] = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(**kwargs)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False

class Feedback(db.Model):
    """Feedback"""

    __tablename__ = "reviews"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                         nullabe=False)
    content = db.Column(db.Text,
                         nullable=False)
    user_id = db.Column(db.Text,
                      db.ForeignKey('users.id'))

    user = db.relationship('User')