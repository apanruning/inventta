#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deployment script.

This script is coded so it can make the deployments automagically in the 
designed servers.

USE: fab <hosts>:<username> <action>
EX: fab staging:admin release
"""

import os
import sys
import tempfile
import datetime
from string import Template
from fabric.api import env, run, local, require, put, sudo, prompt, cd

BASE_DIR = os.path.dirname(__file__)

WSGI_TEMPLATE = Template('''
# -*- coding: utf-8 -*-
import sys, os, site

site.addsitedir('$virtual_env/lib/python2.6/site-packages/')

# Add a custom Python path.
sys.path.append('$deploy_dir')
sys.path.insert(0,'$deploy_dir/apps')

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "production"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
    ''')

def development():
    env.hosts = ["localhost"]
    env.project_name = BASE_DIR.split('/')[-1:].pop()
    env.deploy_dir = '/opt/sites/%s' %env.project_name
    env.virtual_env = '/venvs/%s' %env.project_name
    env.apache_command = 'apache2ctl restart'

def staging():
    pass
    
def production(username="cmonetti", hosts=["inventta.com.ar"]):
    env.user = username
    env.hosts = hosts
    env.project_name = BASE_DIR.split('/')[-1:].pop()
    env.deploy_dir = '/home/cmonetti/webapps/inventta/src/inventta'
    env.virtual_env = '/home/cmonetti/webapps/inventta/venv'
    env.apache_command = '/home/cmonetti/webapps/inventta/apache2/bin/restart'
    
def write_template(file_name, template_name):
    '''
    Pretty much self explanatory
    '''
    template = Template(open(template_name).read())
    rendered_file = open(file_name, 'w')
    rendered_file.write(template.safe_substitute(env))
    rendered_file.close()

    return rendered_file

def release(rev='HEAD'):
    """Creates a tarball, uploads it and decompresses it in the rigth path."""
    require("hosts", provided_by=[development, staging, production])    
    tar = "%s-%s.tar.gz" % (env.project_name ,datetime.datetime.now().strftime("%Y%m%d%H%M%S"),)
    local("git archive %s| gzip > %s" %(rev,tar))
    put(tar, tar)
    run("tar xfz %s -C %s" % (tar, env.deploy_dir))
    run("rm %s" %tar)
    local("rm %s" %tar)

def apache_restart():
    """Restarts the program in the servers."""
    require("hosts", provided_by=[development, staging, production])
    run(env.apache_command)
