import click
from flask.cli import with_appcontext
from models import User
from extensions import db

@click.command('make-admin')
@click.argument('username')
@with_appcontext
def make_admin(username):
    """Promouvoir un utilisateur en administrateur."""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f"Utilisateur {username} non trouvé.")
        return
    
    user.is_admin = True
    db.session.commit()
    click.echo(f"L'utilisateur {username} est maintenant administrateur.") 