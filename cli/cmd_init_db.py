import click
from flask import current_app
from flask.cli import with_appcontext

from sqlalchemy_utils import database_exists, create_database

from src.extensions import db as database
from src.models.user import User


@click.group()
@with_appcontext
def init_db():
    """ Run MYSQL related tasks. """
    pass


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
@with_appcontext
@click.pass_context
def init(ctx, with_testdb):
    """
    Initialize the database.

    :param with_testdb: Create a test database
    :return: None
    """
    database.drop_all()
    User.__table__.create(database.session.bind)

    if with_testdb:
        db_uri = '{0}_test'.format(current_app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(db_uri):
            create_database(db_uri)

    ctx.invoke(seed)

    return None


@click.command()
@with_appcontext
def seed():
    """
    Seed the database with an initial user.

    :return: User instance
    """
    if User.find_by_identity(current_app.config['SEED_ADMIN_EMAIL']) is not None:
        return None

    params = {
        'role': User.ROLE_ADMIN,
        'username': current_app.config['SEED_ADMIN_USERNAME'],
        'email': current_app.config['SEED_ADMIN_EMAIL'],
        'password': current_app.config['SEED_ADMIN_PASSWORD']
    }

    return User(**params).save()


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
@click.pass_context
def reset(ctx, with_testdb):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init, with_testdb=with_testdb)
    ctx.invoke(seed)

    return None


init_db.add_command(init)
init_db.add_command(seed)
init_db.add_command(reset)
