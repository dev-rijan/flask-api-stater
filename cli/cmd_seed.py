import click
import random

from datetime import datetime

from faker import Faker
from flask import current_app
from flask.cli import with_appcontext

from src.extensions import db
from src.models.user import User

fake = Faker()


def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo('Created {0} {1}'.format(count, model_label))

    return None


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is much more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :return: None
    """
    model.query.delete()
    db.session.commit()
    db.engine.execute(model.__table__.insert(), data)

    _log_status(model.query.count(), label)

    return None


@click.group()
@with_appcontext
def seed():
    """ Add items to the database. """
    pass


@click.command()
@with_appcontext
def users():
    """
    Generate fake users.
    """
    random_emails = []
    data = []

    click.echo('Processing...')

    # Ensure we get about 100 unique random emails.
    for i in range(0, 99):
        random_emails.append(fake.email())

    random_emails.append(current_app.config['SEED_ADMIN_EMAIL'])
    random_emails = list(set(random_emails))

    while True:
        if len(random_emails) == 0:
            break

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        created_at = datetime.utcfromtimestamp(
            float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        random_percent = random.random()

        if random_percent >= 0.05:
            role = 'user'
        else:
            role = 'admin'

        email = random_emails.pop()

        random_trail = str(int(round((random.random() * 1000))))
        username = fake.first_name() + random_trail

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        params = {
            'created_at': created_at,
            'updated_at': created_at,
            'role': role,
            'email': email,
            'username': username,
            'password': User.encrypt_password('password')
        }

        # Ensure the seeded admin is always an admin with the seeded password.
        if email == current_app.config['SEED_ADMIN_EMAIL']:
            password = User.encrypt_password(current_app.config['SEED_ADMIN_PASSWORD'])

            params['role'] = 'admin'
            params['password'] = password

        data.append(params)

    return _bulk_insert(User, data, 'users')


@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(users)

    return None


seed.add_command(users)
seed.add_command(all)
