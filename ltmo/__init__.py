# -*- coding: utf-8 -*-

import os
import json
import settings
from flask import Flask
from flaskext.markdown import Markdown
from uuid import uuid4

app = Flask('ltmo', static_path='/media')
app.config.from_object(settings)

Markdown(app)

import ltmo.views
import ltmo.models
import ltmo.forms
