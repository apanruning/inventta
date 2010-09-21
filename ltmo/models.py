# -*- coding: utf-8 -*-

from flaskext.sqlalchemy import SQLAlchemy, BaseQuery
from ltmo import app
from datetime import datetime

from markdown import markdown
from jinja2.filters import do_striptags

db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String(), unique=True)

    def __repr__(self):
        return self.name
    
class Leak(db.Model):
    __tablename__ = 'leaks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    created = db.Column(db.DateTime)
    tags = db.Column(db.String(length=50))
    author = db.Column(db.String(length=50))
    def __init__(self, description, tags, author, **args):
        self.description = description
        self.tags = tags
        self.author = author
        self.created = datetime.now()
        
    def __repr__(self):
        return do_striptags(markdown(self.description))[:150]
    
    

class Tag(db.Model):
    '''
    Stolen from simblin (http://github.com/eugenkiss/Simblin.git)
    Thank you guys
    '''    
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    
    @classmethod
    def get_or_create(cls, tag_name):
        """Only add tags to the database that don't exist yet. If tag already
        exists return a reference to the tag otherwise a new instance"""
        tag = cls.query.filter(cls.name==tag_name).first()
        if not tag:
            tag = cls(tag_name)
        return tag
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name  
        
#    def leaks_count(self):
#        """Return the number of posts with this tag"""
#        return self.leaks.count()
    

    
def syncdb(app):
    with app.test_request_context():
        # The context is needed so db can access the configuration of the app
        db.create_all()
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    return "Initialized new empty database in %s" % db_uri



