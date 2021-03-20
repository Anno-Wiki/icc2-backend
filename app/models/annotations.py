from app import db
from app.models.mixins import Base

class Annotation(Base):
    """The Annotation class.

    Inherits
    --------
    Base

    Attributes
    ----------
    """
    bookid = db.Column(db.Integer)
    open_char = db.Column(db.Integer)
    close_char = db.Column(db.Integer)
    text = db.Column(db.Text)
