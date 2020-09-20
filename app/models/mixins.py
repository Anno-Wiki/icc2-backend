from app import db

from sqlalchemy.ext.declarative import declared_attr, as_declarative

@as_declarative()
class Base(db.Model):
    """This Base class does nothing. It is here in case I need to expand
    implement something later. I feel like it's a good early practice.

    Attributes
    ----------
    id : int
        The basic primary key id number of any class.

    Notes
    -----
    The __tablename__ is automatically set to the class name lower-cased.
    There's no need to mess around with underscores, that just confuses the
    issue and makes programmatically referencing the table more difficult.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
