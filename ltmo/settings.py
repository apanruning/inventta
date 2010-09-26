# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(__file__)

DEBUG = False

ADMINS = (
    ('etnalubma', 'francisco.herrero@gmail.com'),
    ('tutuca', 'maturburu@gmail.com'),
    ('ewock', 'onetti.martin@gmail.com'),
    ('sancho', 'santiago.videla@gmail.com'),
)

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/ltmo.db' % BASE_DIR

SECRET_KEY = '7$57#ttr-tzqr*dt$l7vac0xt&1+i=gi^-y8bnsba$i%ci^nrd'

from local_settings import *
