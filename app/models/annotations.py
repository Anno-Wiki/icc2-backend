from app import db
from app.models.mixins import Base

class Annotation(Base):
    bookid = db.Column(db.Integer)
    open_char = db.Column(db.Integer)
    close_char = db.Column(db.Integer)
    author = db.Column(db.String)

class Edit(Base):
    annotation_id = db.Column(db.Integer, db.ForeignKey('annotation.id'),
                              index=True)
    text = db.Column(db.Text)
    editor = db.Column(db.String)
