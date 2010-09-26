# -*- coding: utf-8 -*-

from flaskext.sqlalchemy import SQLAlchemy, BaseQuery
from ltmo import app
from datetime import datetime

from markdown import markdown
from jinja2.filters import do_striptags

db = SQLAlchemy(app)

class Author(db.Model):
    '''
    Used for profile and simple auth.
    '''
    #FIXME: Lo usamos sólo para mostrar chiches, usar OAuth, OpenID o algo así

    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String(), unique=True)

    def __repr__(self):
        return self.name
    
class Leak(db.Model):
    '''
    El derrame, la razón misma de nuestra existencia.
    
    Pongo el sql que genera la versión django como referencia
    
    BEGIN;
    CREATE TABLE "ltmo_leak" (
        "id" serial NOT NULL PRIMARY KEY,
        "slug" varchar(50) NOT NULL UNIQUE,
        "description" text NOT NULL,
        "author" varchar(20) NOT NULL,
        "created" timestamp with time zone NOT NULL,
        "changed" timestamp with time zone NOT NULL,
        "tags" varchar(255) NOT NULL,
        "metadata" text NOT NULL
    )
    ;
    COMMIT;

    '''
    __tablename__ = 'ltmo_leaks'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(length=50))
    description = db.Column(db.Text)
    created = db.Column(db.DateTime)
    changed = db.Column(db.DateTime)
    tags = db.Column(db.String(length=255))
    author = db.Column(db.String(length=20))
    title = db.Column(db.String(length=125))
    leak_metadata = db.Column(db.Text) # tiro en el pie: SA tiene un atributo 
                                       # metadata, :(
    
    def __init__(self, description, tags, author, *args, **kwargs):
        self.description = description
        self.tags = tags
        self.author = author
        self.changed = datetime.now()
        self.title = do_striptags(markdown(self.description))[:125]
        
        if not self.created:
            self.created = datetime.now()
        
        
        if 'metadata' in args:
            import ipdb; ipdb.set_trace()
    def __repr__(self):
        return self.title
    
class Tag(db.Model):
    '''
    Stolen from simblin (http://github.com/eugenkiss/Simblin.git)
    Should be in a separated app like an extension
    '''    
    __tablename__ = 'tagging_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    
    @classmethod
    def get_or_create(cls, tag_name):
        '''Only add tags to the database that don't exist yet. If tag already
        exists return a reference to the tag otherwise a new instance'''
        tag = cls.query.filter(cls.name==tag_name).first()
        if not tag:
            tag = cls(tag_name)
        return tag
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name  
        
#    def leaks_count(self):
#        '''Return the number of posts with this tag'''
#        return self.leaks.count()
    



