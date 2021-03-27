import time

from datetime import datetime

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
    auth0id = db.Column(db.String(64), index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.displayname}>"

    def __str__(self):
        return self.displayname

