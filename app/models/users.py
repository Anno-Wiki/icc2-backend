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
    # bare necessities
    displayname = db.Column(db.String(64), index=True)
    auth0id = db.Column(db.String(64), index=True)

    # info
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # security
    locked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.displayname}>"

    def __str__(self):
        return self.displayname

