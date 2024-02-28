from flask.cli import FlaskGroup
from app import app, db
from app.models.accounts import Account
from app.models.history import History
from app.models.plantinfo import PlantInfo
from app.models.community import Community


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()




if __name__ == "__main__":
    cli()