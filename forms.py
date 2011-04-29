# -*- coding: utf-8 -*-

from django import forms
from tagging.forms import TagField

from inventta.models import Idea


class IdeaForm(forms.ModelForm):
    description = forms.CharField(
            widget=forms.Textarea,
            help_text='''
            *itálicas*`*itálicas*

            **negritas**` **negritas**

            [link](http://inventta.com.ar)

            * item 1
            * item 2

            `> texto citado`
            '''
        )
    tags = TagField(required=True)    
    class Meta:
        model = Idea
        exclude = ['rendered',]
