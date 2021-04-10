from datetime import datetime as dt

from app import db
from app.models.mixins import Base

class Annotation(Base):
    bookid = db.Column(db.Integer)
    author = db.Column(db.String)

    created = db.Column(db.DateTime)

    edits = db.relationship('Edit', back_populates='annotation')

    HEAD = db.relationship('Edit',
                           primaryjoin='Edit.annotation_id==Annotation.id',
                           uselist=False)

    def __init__(self, book, author, open, close, text, *args, **kwargs):
        self.created = dt.now()
        self.bookid = book
        self.author = author
        super().__init__(*args, **kwargs)
        self.edits.append(Edit(author, open, close, text))


class Edit(Base):
    annotation_id = db.Column(db.Integer, db.ForeignKey('annotation.id'),
                              index=True)
    text = db.Column(db.Text)
    editor = db.Column(db.String)

    open = db.Column(db.Integer)
    close = db.Column(db.Integer)

    created = db.Column(db.DateTime)

    annotation = db.relationship('Annotation', back_populates='edits')

    def __init__(self, editor, open, close, text, *args, **kwargs):
        self.editor = editor
        self.open, self.close = open, close
        self.text = text
        self.created = dt.utcnow()
        super().__init__(*args, **kwargs)
