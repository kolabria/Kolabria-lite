from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login

from mongoengine.django.auth import User

from kolabria.login.forms import UserCreationForm
from kolabria.walls.models import Wall


def register(request):
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
        return render_to_response('login/register-success.html',
                          context_instance=RequestContext(request))
    return render_to_response('login/register.html', data,
                              context_instance=RequestContext(request))
