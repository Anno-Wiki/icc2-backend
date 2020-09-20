import time
import jwt

from datetime import datetime
from hashlib import md5

from app import db
from app.models.mixins import Base

class User(Base):
    """The User class.

    Inherits
    --------
    Base

    Attributes
    ----------
    """
    # bare necessities
    displayname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))

    # info
    bio = db.Column(db.Text)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # security
    locked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.displayname}>"

    def __str__(self):
        return self.displayname

    def avatar(self, size):
        """A link to the gravatar for this user."""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


    # Password routes
    def set_password(self, password):
        """Set the password for the user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check that the password provided is the user's current password."""
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        """Generate a reset_password token for the user's emailed link to reset
        the password.
        """
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        """A static method to verify a reset password token's validity."""
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
