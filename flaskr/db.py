import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

#function for call the database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db 

#function for close the DB
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#init / make DB with schema.sql file 
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#make custome command with flask @click.command
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

#register the app to factory function
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)