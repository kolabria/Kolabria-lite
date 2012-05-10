from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from mongoengine.django.auth import User
from account.models import Account
from login.models import UserProfile
from walls.models import Wall
from appliance.models import Box
from appliance.forms import NewBoxForm, BoxForm, PubWallForm, UnsubWallForm
from datetime import datetime

#import ipdb

@login_required
def appliances(request):
    boxes = Box.objects.all()
    form = NewBoxForm(request.POST or None)
    if form.is_valid():
#        ipdb.set_trace()
        box_name = request.POST['name']
        box_location = request.POST['location']
        profile = UserProfile.objects.filter(
                                  user=request.user)[0]
        new_box = Box.objects.create(company=profile.company, owner=request.user,
                                     name=box_name, location=box_location)
        new_box.save()
        msg = '%s %s %s' % (new_box.name, new_box.location,
                            profile.company.company) 
        messages.success(request, msg)
        return HttpResponseRedirect('/devices/')
#        msg = 'name: %s   |   company: %s' % (company_name, company)
#        messages.succes(request, msg)
    data = {'title': 'Kolabria - My Appliances',
            'boxes': boxes, 
            'form': form, }
    return render_to_response('appliance/devices.html', data,
                       context_instance=RequestContext(request))

@login_required
def remove_box(request, bid):
    info = """
           Details:
           user: %s\n
           username: %s\n
           company: %s\n
           box: %s\n
           box_name: %s\n
           """
    profile = UserProfile.objects.get(user=request.user)
    box = Box.objects.get(id=bid)
    msg0 = info % (request.user, request.user.username, 
                   profile.company, box.id, box.name)
    messages.info(request, msg0)
    box.delete()
    msg1 = 'Successfully removed appliance: %s %s %s' % (box.id,
                                                        box.name,
                                                        box.location)
    messages.success(request, msg1)
    return HttpResponseRedirect('/devices/')


def auth_box(request):
#    ipdb.set_trace()
    user_agent = request.META['HTTP_USER_AGENT']
    data = {'title': 'Kolabria - Valid Appliance ',}
    if user_agent[:4] == 'WWA-':
        box_id = user_agent[4:]
        try:
            box = Box.objects.get(id=box_id)
            # authenticate box as user 
#            user = User.objects.get(username=box_id)
#            user.check_password(box_id)
#            login(request, user)
#            msg = "Success! Appliance ID (%s) == Valid username (%s)\n" % \
#                                                     (box_id, user.username)
            msg = "Recognized Appliance: %s id=%s" % (box.name, box_id)
            messages.success(request, msg)
            return HttpResponseRedirect('/box/%s/' % box_id)
        except Box.DoesNotExist:
            messages.error(request, 'Appliance %s not recognized' % box_id)
            return HttpResponseRedirect('/')
    messages.error(request, 'Access to url /box/ Unauthorized')
    return HttpResponseRedirect('/')


def the_box(request, bid):
#    ipdb.set_trace()
    unsub_form = UnsubWallForm()
    pub_form = PubWallForm()
    box = Box.objects.get(id=bid)
    box_name = box.name
    walls = Wall.objects.filter(published=str(box.id))

    if box.active_wall:
        active = Wall.objects.get(id=box.active_wall)
    else:
        active = None

    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,
            'bid': bid,
            'active': active,
            'walls': walls, 
            'unsub_form': unsub_form }

    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def active_wall(request, wid):
    wall = Wall.objects.get(id=wid)
    data = {'title': 'Kolabria WikiWall Appliance | Active Wall: %s' % wall.name,
            'wall': wall, }
    return render_to_response('appliance/boxwall.html', data,
                              context_instance=RequestContext(request))

def pubwall(request, bid):
#    ipdb.set_trace()
    box = Box.objects.get(id=bid)
    box_name = box.name
    walls = [ Wall.objects.get(id=wid) for wid in box.walls ]

    pub_form = PubWallForm(request.POST or None)

    if pub_form.is_valid():
        wid = request.POST['wid']
        wall = Wall.objects.get(id=wid)
        box = Box.objects.get(id=bid)
        box.active_wall = request.POST['wid']
        box.save()
        messages.success(request, 'Wall: %s Activated on appliance: %s' % \
                                                         (wall.name, box.name))
        return HttpResponseRedirect('/box/%s' % box.id)

    pub_form.initial['publish'] = True 

    data = {'title': 'Kolabria | Publish WikiWall',
            'box': box,
            'bid': bid,
            'box_name': box_name,
            'walls': walls,
            'pub_form': pub_form, }

    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def unsubwall(request, bid):
    unsub_form = UnsubWallForm(request.POST or None)
    if unsub_form.is_valid():
        box = Box.objects.get(id=bid)
        wid = request.POST.get('wid')
        wall = Wall.objects.get(id=wid)
        if bid in wall.published:
            wall.published.remove(bid)
            wall.save()
            messages.success(request, 'Box %s removed from wall.published %s' % \
                                                                  (box.name, wall.name))
        box = Box.objects.get(id=bid)
        if wid in box.walls:
            box.walls.remove(wid)
            box.active_wall = ''
            box.save()
            messages.success(request, 'Box %s Unsubscribed from box.wall: %s' % \
                                                                 (box.name, wid))
        return HttpResponseRedirect('/box/')
    
    data = { 'bid': bid, 'unsub_form': unsub_form } #, 'walls': walls }
    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def id_appliance(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'bux': box,}
    render_to_response('apppliance/id-appliance.html', data,
                       context_instance=RequestContext(request))
