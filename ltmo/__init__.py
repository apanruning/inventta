# -*- coding: utf-8 -*-

import os
import json
import settings
from flask import Flask
from flask import request, session, g, redirect, url_for, render_template, flash
from flaskext.markdown import Markdown
from uuid import uuid4

app = Flask('ltmo', static_path='/media')
app.config.from_object(settings)

Markdown(app)



@app.context_processor
def about():
    f = open(os.path.join(app.config['BASE_DIR'], 'ABOUT'), 'r')
    return {
        'about':f.read().decode('utf-8'),
    }
    
@app.route('/', methods=['POST', 'GET'])
def index():
    from models import Leak
    object_list = Leak.query.all()
    if request.method == 'POST':
        data = json.loads(request.data)
        import ipdb; ipdb.set_trace()
        leak = Leak(data)      
        return render_template('success.json')
         
    return render_template('index.html', object_list=object_list)
