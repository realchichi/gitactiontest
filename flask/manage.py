from flask.cli import FlaskGroup


from app import app, db
from app.models.contact import Contact


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()




if __name__ == "__main__":
    cli()