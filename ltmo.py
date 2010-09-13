# -*- coding: utf-8 -*-

import os
import json
import settings
from couchdb import Server
from flask import Flask
from flask import request, session, g, redirect, url_for, render_template, flash
from flaskext.markdown import Markdown
from uuid import uuid4


app = Flask('ltmo', static_path='/media')
app.config.from_object(settings)

Markdown(app)
couch_server = Server(app.config['COUCHDB_SERVER'])

try :
    db = couch_server['ltmo']
except KeyError: 
    db = couch_server.create('ltmo')

@app.context_processor
def about():
    f = open(os.path.join(app.config['BASE_DIR'], 'ABOUT'), 'r')
    return {
        'about':f.read().decode('utf-8'),
    }
    
@app.route('/', methods=['POST', 'GET'])
def index():
    func_str = "function(d) { if (d.description.length>4) emit(d,null);}"
    rows = db.view('_all_docs', include_docs=True)
    object_list = [row.doc for row in rows]
    if request.method == 'POST':
        doc_id = uuid4().hex
        db[doc_id] = json.loads(request.data)      
        return render_template('success.json')
         
    return render_template('index.html', object_list=object_list)
