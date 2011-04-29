# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from inventta.models import Idea

class IdeaFeed(Feed):
    title = "Recientemente derramado"
    link = "/"
    description = "Cosas publicadas recientemente en el fantastico inventta"
    description_template = 'feeds/description.html'

    def items(self):
        return Idea.objects.order_by("-created")[:15]

    def item_title(self, item):
        return item.title or ' '

    def item_description(self, item):
        return item.description
