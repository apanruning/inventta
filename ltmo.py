# -*- coding: utf-8 -*-

import os
import json
import settings
from flask import Flask
from flask import request, session, g, redirect, url_for, render_template, flash
#from flaskext.couchdb import CouchDBManager, ViewDefinition
from couchdb import Server
from github2.client import Github

app = Flask('ltmo', static_path='/media')
app.config.from_object(settings)

couch_server = Server('http://127.0.0.1:5984/')
try :
    db = couch_server['ltmo']
except KeyError: 
    db = couch_server.create('ltmo')

@app.context_processor
def about():
    github = Github(username=app.config['GITHUB_USER'], api_token=app.config['GITHUB_API_TOKEN'])
    f = open(os.path.join(app.config['BASE_DIR'], 'ABOUT'), 'r')
    return {
        'about':str(f.read()),
        'repository':github.repos.show("tutuca/ltmo")
    }
    
@app.route('/', methods=['POST', 'GET'])
def index():
    func_str = "function(d) { if (d.description.length>4) emit(d.description,null);}"
    result = db.query(func_str)
    if request.method == 'POST':
       leak = db.create(**json.loads(request.data))
       
    return render_template('index.html', object_list=result)
