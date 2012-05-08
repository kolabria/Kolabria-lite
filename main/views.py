#u -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages

def home(request):
    data = {'title': 'Kolabria - Real-time collaboration, made simple',}
    return render_to_response('main/home.html', data,
                              context_instance=RequestContext(request)) 
