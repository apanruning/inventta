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
    
class Leak(db.Model):
    __tablename__ = 'leaks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship('Tag', secondary='leak_tags', 
        backref=db.backref('leaks', lazy='dynamic'))

    def __repr__(self):
        return do_striptags(markdown(self.description))[:150]

leak_tags = db.Table('leak_tags', db.Model.metadata,
    db.Column('leak_id', db.Integer, 
              db.ForeignKey('leaks.id', ondelete='CASCADE')),
    db.Column('tag_id', db.Integer,
              db.ForeignKey('tags.id', ondelete='CASCADE')))

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
    
    def leaks_count(self):
        """Return the number of posts with this tag"""
        return self.leaks.count()
    
    def __repr__(self):
        return self.name
    
def syncdb(app):
    with app.test_request_context():
        # The context is needed so db can access the configuration of the app
        db.create_all()
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    return "Initialized new empty database in %s" % db_uri



