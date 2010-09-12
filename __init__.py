# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template

app = Flask(__name__, static_path='/media')
app.config.from_envvar('APP_SETTINGS')

import ltmo.views


