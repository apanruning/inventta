# -*- coding: utf-8 -*-

import os
import json
from markdown import markdown
from werkzeug.contrib.atom import AtomFeed
from flask import request, session, redirect, url_for, render_template, flash
from ltmo import app
from ltmo.models import Leak, db
from ltmo.forms import LeakForm


@app.route('/', methods=['POST', 'GET'])
def index():
    form = LeakForm()
    object_list = Leak.query.order_by('created')
    if request.method == 'POST':
        data = json.loads(request.data)
        leak = Leak(**data)
        db.session.add(leak)
        db.session.commit()
        return render_template('success.json')

    return render_template(
        'index.html',
        object_list=object_list,
        form=form,
    )


@app.route('/feed')
def atom_feed():
    feed = AtomFeed(
        "Derrames publicados",
        feed_url=request.url,
        url=request.host_url,
    )

    for leak in Leak.query.order_by('created'):
        leak_url = '%s%s' % (request.host_url, leak.id)
        feed.add(
            leak.title,
            markdown(leak.description),
            content_type='html',
            author=leak.author,
            url=leak_url,
            id=leak.id,
            updated=leak.created,
        )
    return feed.get_response()
