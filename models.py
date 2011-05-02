# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from tagging.fields import TagField
from tagging.utils import parse_tag_input

from django.contrib import admin
from django.template.defaultfilters import striptags, slugify
from markdown import markdown

class Idea(models.Model):
    slug = models.SlugField(editable=False, blank=True, null=True)
    title = models.CharField(max_length=126, blank=True, null=True)
    description = models.TextField()
    rendered = models.TextField(null=True, blank=True, editable = False)
    author = models.SlugField(max_length=20, default='anon')
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    tags = TagField()
    metadata = models.TextField(default='', null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.title or u'sin título'

    @models.permalink
    def get_absolute_url(self):
        return ('idea_detail', [parse_tag_input(self.tags)[0], self.id])

    def save(self):
        self.rendered = markdown(
            self.description, 
            ['video', 'codehilite', 'urlize']
        )
        self.tags = ','.join([slugify(x) for x in parse_tag_input(self.tags)])
        self.slug = '%s-%s' %(slugify(self.title[:30]) or 'sin-titulo', self.pk)
        super(Idea, self).save()
        
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'tags','author', 'is_draft', 'created', 'changed')
    list_filter = ('author', 'created', 'is_draft')

admin.site.register(Idea, IdeaAdmin)


class Comment(Idea):
    parent = models.ForeignKey('Idea', null=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('comment_detail', [self.id])
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'parent','author', 'is_draft', 'created', 'changed')
    list_filter = ('author', 'created', 'is_draft')

admin.site.register(Comment, CommentAdmin)
