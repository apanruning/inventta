# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from tagging.models import Tag

from inventta.forms import IdeaForm, CommentForm
from inventta.models import Idea, Comment


def index(request):
    queryset = Idea.objects.all().order_by('pk')
    if not request.user.is_staff:
        queryset = queryset.exclude(is_draft=True)
    form = IdeaForm()

    if request.method == 'POST':
        next = request.POST['next']
        form = IdeaForm(request.POST)

        if form.is_valid():
            idea = form.save()
            messages.success(
                request, 
                u'Mensaje publicado con exito.'
            )
            return redirect(next)
        else :
            return idea_new(request, form_instance=form)            
    return render(
        request,
        'master.html',
        {
            'idea_form': form,
            'object_list': queryset,
        }
    )

def idea_detail(request, tag_name, object_id):
    queryset = Idea.objects.all()
    form = IdeaForm(initial={'tags':tag_name})
    idea = get_object_or_404(Idea, pk=object_id)

    if request.method == 'POST':
        next = request.POST['next']
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            idea = form.save()
            messages.success(request, 'Actualizaste el #%s' %(object_id))
            return redirect(next)
        else :
            return idea_new(
                request,
                tag_name=tag_name,
                object_id=object_id,
                form_instance=form
            )
    return render(
        request,
        'detail.html',
        {
            'idea_form': form,
            'tag': tag_name,
            'object': idea,
            'object_list': queryset.filter(tags__icontains=tag_name),
        }
    )

@login_required
def idea_new(request, tag_name=None, object_id=None, form_instance=None):
    form = IdeaForm()
    
    if object_id:
        idea = get_object_or_404(Idea, pk=object_id)
        form = IdeaForm(instance=idea)
    else :
        idea = None

    if form_instance:
        form = form_instance
                
    return render(
        request, 
        'idea_form.html',
        {
            'form': form,
            'instance': idea,
            'tag_name': tag_name,
        }
    )

def comment_list(request):
    queryset = Comment.objects.all().order_by('changed')
    if not request.user.is_staff:
        queryset = queryset.exclude(is_draft=True)
    form = CommentForm()

    if request.method == 'POST' and request.POST['honeypot'] == '':
        next = request.POST['next']
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tags = u'comentario,'
            comment.save()
            messages.success(
                request, 
                u'Mensaje publicado con exito.'
            )
            return redirect(next)
        else :
            return comment_new(request, form_instance=form)
    return render(
        request,
        'master.html',
        {
            'comment_form': form,
            'object_list': queryset,
        }
    )

def comment_detail(request, object_id):
    queryset = Comment.objects.all()
    form = CommentForm()
    comment = get_object_or_404(Comment, pk=object_id)

    if request.method == 'POST':
        next = request.POST['next']
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tags = u'comentario,'
            comment.save()
            messages.success(request, 'Actualizaste el #%s' %(object_id))
            return redirect(next)
        else :
            return comment_new(
                request, 
                object_id=object_id,
                form_instance=form
            )
    return render(
        request,
        'detail.html',
        {
            'comment_form': form,
            'object': comment,
            'object_list': queryset,
        }
    )

def comment_new(request, object_id=None, form_instance=None):
    form = CommentForm()
    if object_id:
        idea = get_object_or_404(Idea, pk=object_id)
        form = CommentForm(instance=idea)

    return render(
        request, 
        'comment_form.html',
        {'form': form}
    )
    
def idea_json(request, tag_name, object_id):
    queryset = Idea.objects.all()
    form = IdeaForm(initial={'tags':tag_name})
    idea = get_object_or_404(Idea, pk=object_id)
    return HttpResponse(
        json.dumps({
            'title':idea.title,
            'author':idea.author,
            'description':idea.description,
            'is_draft':idea.is_draft,
            'tags': idea.tags
        }),
        
        mimetype="application/json"
    )
        
def by_tag(request, tag_name=None):
    queryset = Idea.objects.all().order_by('tags')
    form = IdeaForm()

    if tag_name:
        queryset = queryset.filter(tags__icontains=tag_name)

    return render(
        request,
        'list.html',
        {
            'form': form,
            'tag_name': tag_name,
            'object_list': queryset.filter(tags__icontains=tag_name),
        }
    )

def tags(request):
    queryset = Tag.objects.all()
    tag_name = request.GET.get('tag_name')
    if tag_name:
        queryset = queryset.filter(name__istartswith=tag_name)
    return HttpResponse(
        json.dumps([x.name for x in queryset]), 
        mimetype="application/json"
    )
    
def profile_detail(request, username):
    queryset = Idea.objects.filter(author__icontains=username).order_by('-created')

    try:
        author = User.objects.get(username__icontains=username)
    except :
        author = None

    return render(
        request,
        'profile.html',
        {
            'author':author,
            'is_me':request.user.username == 'username',
            'object_list': queryset,
        }
    )

def login(request):
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username', 'None')
        password = request.POST.get('password', 'None')
        user = authenticate(username=username, password=password)
        next = request.POST.get('next')
        message = ''
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'bienvenido %s' %(user, ))
                
            
        return HttpResponse(
            json.dumps({
                'next': next,
            }),
            
            mimetype="application/json"
        )

