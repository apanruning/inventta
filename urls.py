# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.contrib.sitemaps import GenericSitemap
from django.contrib import admin
from django.views.generic import TemplateView

from inventta.feeds import IdeaFeed
from inventta.models import Idea
from inventta.forms import CommentForm, IdeaForm

admin.autodiscover()

info_dict = {
    'queryset': Idea.objects.all(),
    'date_field': 'created',
}

sitemaps = {
    'ideas': GenericSitemap(info_dict, priority=0.6),
}

urlpatterns = patterns('inventta.views',
    (r'^$','index',{},'index'),
    (r'^idea/$','index',{},'index'),
    (r'^idea/new$','idea_new',{},'idea_new'),
    (r'^idea/(?P<tag_name>[\w-]+)$','by_tag',{},'tag'),
    (r'^idea/(?P<tag_name>[\w-]+)/(?P<object_id>\d+)$','idea_detail',{},'idea_detail'),
    (r'^idea/(?P<tag_name>[\w-]+)/(?P<object_id>\d+)/edit$','idea_new'),
    (r'^idea/(?P<tag_name>[\w-]+)/(?P<object_id>\d+).json$','idea_json',{},'idea_json'),
    (r'^comentarios/$','comment_list',{},'comment_list'),
    (r'^comentarios/new$','comment_new',{},'comment_new'),
    (r'^comentarios/(?P<object_id>\d+)$','comment_detail',{},'comment_detail'),
    (r'^comentarios/(?P<object_id>\d+)/edit$','comment_new'),

    (r'^tags/','tags',{},'tags'),
    (r'^~(?P<username>\w+)/$','profile_detail', {}, 'author_detail'),
    (r'^in/$', 'login', {}, 'login'),
)
urlpatterns +=patterns('django.contrib.auth.views',
    (r'^out/$', 'logout', {'next_page':'/'}, 'logout'),

)
urlpatterns += patterns('',
    (r'^help/$', TemplateView.as_view(template_name='help.html')),
)
urlpatterns += patterns('',
    (r'^gerencia/', include(admin.site.urls)),
    (r'^feed/$',IdeaFeed()),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /media/*", mimetype="text/plain")),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', 
        {'sitemaps': sitemaps})
)
