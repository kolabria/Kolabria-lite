from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from kolabria.account.forms import NewAccountForm, NewBoxForm
from kolabria.account.models import Account
from kolabria.appliance.models import Box
from mongoengine.django.auth import User

import ipdb

def create(request):
    form = NewAccountForm(request.POST or None)
    if form.is_valid():
        # also attach the contact information to the anonymous request.user
        new_user.first_name = request.POST['first_name']
        new_user.last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password2']
        new_user = User.create_user(username=username, email=email,
                                    password=password)
        new_user.save()

        # create the account instance
        new_account = Account()
        new_account.company = request.POST['company_name']
        new_account.admin = new_user
        new_account.save()
        messages.success(request, new_account)

        # now authenticate and login user
        auth_user = authenticate(username=username, password=password)
        login(request=request, user=auth_user)
        messages.success(request, 'Successfully logged in as %s' % \
                                                           auth_user.username)
        return HttpResponseRedirect('/welcome/')

    data = {'title': 'Kolabria - Create a new Account ', 'form': form, }
    return render_to_response('account/create.html', data,
                              context_instance=RequestContext(request))


@login_required
def welcome(request):
    form = NewBoxForm(request.POST or None)
    if form.is_valid():
        name = request.POST['name']
        location = request.POST['location']
        box = Box.objects.create(name=name, location=location)
        box.save()
        msg = '%s %s %s' % (box.id, box.name, box.location)
        messages.info(request, msg)
        messages.info(request, request.POST)
        return HttpResponseRedirect('/welcome/')

    data = {'title': 'Kolabria - New Account Confirmation', 'form': form, }
    return render_to_response('account/welcome.html', data,
                              context_instance=RequestContext(request))
