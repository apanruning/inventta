# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(__file__)

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('etnalubma', 'francisco.herrero@gmail.com'),
    ('tutuca', 'maturburu@gmail.com'),
    ('ewock', 'onetti.martin@gmail.com'),
)

MANAGERS = ADMINS

SQLALCHEMY_DATABASE_URI = 'sqlite://%s/ltmo.db' % BASE_DIR

COUCHDB_DATABASE = 'ltmo'

SECRET_KEY = '7$57#ttr-tzqr*dt$l7vac0xt&1+i=gi^-y8bnsba$i%ci^nrd'

from local_settings import *