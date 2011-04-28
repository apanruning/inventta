from django import forms
from tagging.forms import TagField

from inventta.models import Idea


class IdeaForm(forms.ModelForm):
    tags = TagField(required=True)    
    class Meta:
        model = Idea
        exclude = ['rendered',]
