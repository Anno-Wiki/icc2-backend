from app import create_app, db
from app.models import classes

app = create_app()

@app.shell_context_processor
def make_shell_context():
    print(db)
    return dict(db=db, **classes)
