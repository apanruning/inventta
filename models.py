# -*- coding: utf-8 -*-

from flaskext.couchdb import Document, Mapping
from flaskext.couchdb import TextField, DateTimeField, ListField, ViewField


class Leak(Document):
    doc_type = 'leak'
    description = TextField()
    author = TextField(default='Anonymous')
    created = DateTimeField()
    changed = DateTimeField()
    tags = ListField(TextField(default='random'))
    metadata = TextField()

    tagged = ViewField('leaks', '''\
        function (doc) {
            if (doc.doc_type == 'leak') {
                doc.tags.forEach(function (tag) {
                    emit(tag, doc);
                });
            };
        }''')


class Author(Document):
    doc_type = 'author'
    description = TextField(default='Anonymous')
    email = TextField()

