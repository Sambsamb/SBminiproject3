import sqlite3

import click
from flask import current_app, g


def get_db():
    # g is a special object that is unique for each request.
    if 'db' not in g:
        # sqlite3.connect() establishes a connection to the file pointed at by the DATABASE configuration key.
        g.db = sqlite3.connect(
            # current_app is another special object that points to the Flask application handling the request.
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row tells the connection to return rows that behave like dicts.
        # This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Functions to run SQL commands from 'schema.sql'
def init_db():
    db = get_db()  # get_db returns a database connection

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')  # defines a command line command called init-db
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the database :)')


# Register with the Application
def init_app(app):
    app.teardown_appcontext(close_db)  # Cleaning up after returning the response
    app.cli.add_command(init_db_command)  # New command that can be called with the flask command


