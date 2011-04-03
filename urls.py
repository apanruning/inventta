from django.conf import settings
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.contrib.sitemaps import GenericSitemap
from django.contrib import admin

from ltmo.feeds import LeakFeed
from ltmo.models import Leak

admin.autodiscover()

info_dict = {
    'queryset': Leak.objects.all(),
    'date_field': 'created',
}

sitemaps = {
    'leaks': GenericSitemap(info_dict, priority=0.6),
}

urlpatterns = patterns('ltmo.views',
    (r'^$','index',{},'index'),
    (r'^(?P<object_id>\d+)$','leak_detail',{},'leak_detail'),
    (r'^leak/$','index',{},'leak_new'),
    (r'^tag/$','by_tag',{},'by_tag'),
    (r'^tag/(?P<tag_name>\w+)$','by_tag',{},'tag'),
    (r'^tags/','tags',{},'tags'),

)
urlpatterns += patterns('django.views.generic',
    (r'^help/$', 'simple.direct_to_template', {'template': 'help.html', 'extra_context':{'title':'Ayuuuudaaaa'},}),
)
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^feed/$',LeakFeed()),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /media/*", mimetype="text/plain")),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', 
        {'sitemaps': sitemaps})

)
urlpatterns += patterns('',
#   url(r'^create/$',
#       views.create_profile,
#       name='profiles_create_profile'),

   url(r'^~(?P<username>\w+)/$','profiles.views.profile_detail', name='author_detail'),
   )
      
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT})
    )
    
