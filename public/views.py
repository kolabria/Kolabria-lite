from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from mongoengine.django.auth import User
from account.models import Account
from account.forms import NewAccountForm
import ipdb


def create(request):
    form = NewAccountForm(request.POST or None)
    if form.is_valid():
#        ipdb.set_trace()
        # create new user and save profile details; save new user
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        company = request.POST['company']
        password = request.POST['password2']
        new_user = User.create_user(username=username, email=email,
                                    password=password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        # create the account instance
        new_account = Account()
        new_account.name = request.POST['company']

        # set new user as admin for account instance; save account
        new_account.admin = new_user
        new_account.save()
        messages.success(request, new_account)

        # authenticate and log in user
        auth_user = authenticate(username=username, password=password)
        login(request=request, user=auth_user)
        messages.success(request, 'Successfully logged in as %s' % \
                                                           auth_user.username)
#        slug = slugify(new_account.name)
        return HttpResponseRedirect('/devices/')

    data = {'title': 'Kolabria - Create a new Account ', 'form': form, }
    return render_to_response('account/create.html', data,
                              context_instance=RequestContext(request))



def public(request):
    data = {'title': 'Kolabria - Homepage', }
    return render_to_response('public/home.html', data,
                              context_instance=RequestContext(request))


