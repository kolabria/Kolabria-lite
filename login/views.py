from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages

from mongoengine.django.auth import User

from login.forms import UserCreationForm
from walls.models import Wall

import ipdb

def register(request):
    ipdb.set_trace()
    form = UserCreationForm(request.POST or None)
    data = {'title': 'Kolabria - Registration Page',
            'form': form,}
    if form.is_valid():
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password2']
        new_user = User.create_user(username=username, email=email,
                                    password=password)
        new_user.save()
        auth_user = authenticate(username=username, password=password)
        login(request=request, user=auth_user)
        messages.success(request, new_user)
        return HttpResponseRedirect('/devices/')
    return render_to_response('login/register.html', data,
                              context_instance=RequestContext(request))
