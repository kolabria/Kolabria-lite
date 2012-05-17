from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from mongoengine.django.auth import User
from account.models import Account
from account.forms import NewAccountForm, JoinMeetingForm
from appliance.models import Box
from walls.models import Wall

import ipdb

def public(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/devices/')
    else:
        return HttpResponseRedirect('/home/')


def home(request):
    data = {'title': 'Kolabria - Homepage', }
    return render_to_response('public/home.html', data,
                              context_instance=RequestContext(request))

def join(request):
    form = JoinMeetingForm(request.POST or None)
    if form.is_valid():
       ipdb.set_trace()
       name = request.POST['name']
       room = request.POST['room']
       code = request.POST['code']
       request.session['name'] = name
       try:
           box = Box.objects.get(box_name=room)
           wall_id = box.active_wall
           wall = Wall.objects.get(id=wall_id)
           if wall.code == int(code):
               request.session['wid'] = str(wall.id)
               messages.success(request, '%s %s %s' % (name, room, code))
               return HttpResponseRedirect('/walls/%s' % str(wall.id))
           else:
               messages.error(request, 'Error: Invalid Code. Please try again.')
               return HttpResponseRedirect('/join/')
       except:
           messages.error(request, 'Error: Device not found. Please try again')
           return HttpResponseRedirect('/join')

    data = {'title': 'Kolabria - Join a WikiWall Meeting', 
            'form': form }
    return render_to_response('public/join.html', data,
                              context_instance=RequestContext(request))
