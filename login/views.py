from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages

from mongoengine.django.auth import User
from login.forms import UserCreationForm
from account.models import Account
from walls.models import Wall

#import ipdb

def register(request):
#    ipdb.set_trace()
    form = UserCreationForm(request.POST or None)
    data = {'title': 'Kolabria - Registration Page',
            'form': form,}
    if form.is_valid():
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password2']
        username = request.POST['username']
        new_user = User.create_user(username=username, email=email,
                                    password=password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        auth_user = authenticate(username=username, password=password)
        login(request=request, user=auth_user)

        new_account = Account()
        new_account.name = request.POST['company']
        new_account.save()
        messages.success(request, new_user)
        messages.success(request, new_account)
        return HttpResponseRedirect('/devices/')
                              context_instance=RequestContext(request))
    return render_to_response('account/create.html', data,
