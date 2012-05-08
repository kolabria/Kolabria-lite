from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from kolabria.users.forms import UserDetailsForm, UpdatePasswordForm
from mongoengine.django.auth import User

import ipdb

@login_required
def profile(request):
    user = request.user
    details_form = UserDetailsForm(request.POST or None)

    if details_form.is_valid():
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        full_name = '%s %s %s' % (user.first_name, user.last_name, user.email)
        messages.success(request, 'Updated user details for %s' % full_name)
        return HttpResponseRedirect('/profile/')

    details_form.initial['first_name'] = request.user.first_name
    details_form.initial['last_name'] = request.user.last_name
    details_form.initial['email'] = request.user.email

    data = {'title': 'Kolabria - Edit Profile', 'details_form': details_form, }
    return render_to_response('users/profile.html', data,
                              context_instance=RequestContext(request))
