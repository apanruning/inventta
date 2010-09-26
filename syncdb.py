#!/usr/bin/env python

from ltmo import app
from ltmo.models import db

def syncdb(app):
    with app.test_request_context():
        # The context is needed so db can access the configuration of the app
        db.create_all()
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    return "Initialized new empty database in %s" % db_uri
    
syncdb(app)
