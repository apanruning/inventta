# -*- coding: utf-8 -*-

import os
import json

from flask import request, session, g, redirect, url_for, render_template, flash
from ltmo import app
from ltmo.models import Leak, db

@app.route('/', methods=['POST', 'GET'])
def index():
    object_list = Leak.query.all()
    if request.method == 'POST':
        data = json.loads(request.data)
        leak = Leak(**data)
        db.session.add(leak)
        import ipdb; ipdb.set_trace()
        db.session.commit()
        return render_template('success.json')
         
    return render_template('index.html', object_list=object_list)
