# -*- coding: utf-8 -*-

import os
import json

from flask import request, session, g, redirect, url_for, render_template, flash
from flaskext.couchdb import CouchDBManager, ViewDefinition
from github2.client import Github
from models import Leak



#manager = CouchDBManager()
#manager.setup(app)

#@app.context_processor
#def about():
#    github = Github(username=app.config['GITHUB_USER'], api_token=app.config['GITHUB_API_TOKEN'])
#    f = open(os.path.join(app.config['BASE_DIR'], 'ABOUT'), 'r')
#    return {
#        'about':str(f.read()),
#        'repository':github.repos.show("tutuca/ltmo")
#    }
#    
#@app.route('/', methods=['POST', 'GET'])
#def index():
#    if request.method == 'POST':
#       leak = Leak(**json.loads(request.data))
#       leak.store()
#       
#    return render_template('index.html')
