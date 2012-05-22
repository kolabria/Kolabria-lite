from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.util import ValidationError

from mongoengine.django.auth import User
from account.models import Account
from login.models import UserProfile
from walls.models import Wall
from appliance.models import Box
from appliance.forms import NewBoxForm, EditBoxForm, BoxForm
from appliance.forms import ShareBoxForm, PubWallForm, UnsubWallForm
from datetime import datetime


@login_required
def appliances(request):
    profile = UserProfile.objects.get(user=request.user)
    boxes = Box.objects.filter(company=profile.company)
    form = NewBoxForm(request.POST or None)
    if form.is_valid():
        box_id = request.POST['box_id']
        box_name = request.POST['box_name']
        profile = UserProfile.objects.filter(
                                  user=request.user)[0]
        new_wall = Wall.objects.create(company=profile.company, box_id=box_id)
        new_wall.save()
        try:
            duplicate = Box.objects.get(box_id=box_id)
        except:
            duplicate = ''

        if duplicate:
            messages.error(request, 'Error: Device already registered with box_id: %s' % box_id)
            return HttpResponseRedirect('/devices/')
        else:
            new_box = Box.objects.create(company=profile.company, owner=request.user,
                                     box_id=box_id, box_name=box_name, 
                                     active_wall=str(new_wall.id))
            new_box.save()
            msg = '%s %s %s' % (new_box.box_id, new_box.box_name,
                                profile.company.company) 
            messages.success(request, msg)
            return HttpResponseRedirect('/devices/')

    data = {'title': 'Kolabria - My Appliances',
            'boxes': boxes,
            'form': form, }
    return render_to_response('appliance/devices.html', data,
                       context_instance=RequestContext(request))

def detail(request, box_id):
    box = Box.objects.get(box_id=box_id)
    edit_form = EditBoxForm(request.POST or None)
    if edit_form.is_valid():
        box.box_name = request.POST['box_name']
        box.save()
        messages.success(request, 'Successfully updated box_id: %s' % box.box_id)
        return HttpResponseRedirect('/devices/edit/%s' % box.box_id)

    share_form = ShareBoxForm(request.POST or None)
    if share_form.is_valid():
        data = request.POST['data']
        try:
            shared_box = Box.objects.get(box_name__iexact=data)
            if shared_box.box_id not in box.sharing:
                box.sharing.append(str(shared_box.box_id))
                box.save()
#            if shared_box.box_id not in box.sharing:
                # and shared_box.box_id != box_id
        except:
            pass

        try:
            shared_box = Box.objects.get(box_id__iexact=data)
            if shared_box.box_id not in box.sharing:
                box.sharing.append(str(shared_box.box_id))
                box.save()
#                messages.success(request, 'Successfully added device: %s to QuickShare' % \
#                                                                          shared_box.box_name)
        except:
            pass
#            msg = 'Error: Device not found matching %s' % data
#            messages.error(request, msg)
        return HttpResponseRedirect('/devices/edit/%s' % box_id)
    print box.sharing
    sharing = [ Box.objects.get(box_id=boxid) for boxid in box.sharing ]
    edit_form.fields['box_name'].initial = box.box_name
    data = {'title': 'Kolabria - My Appliances',
            'box': box,
            'editform': edit_form,
            'shareform': share_form,
            'sharing': sharing, 
            }
    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def wikiwall(request, box_id):
    if 'auth' not in request.session:
        messages.warning(request, 'Error: Not Authorized')
        return HttpResponseRedirect('/join/')
    else:
        wall = Wall.objects.get(id=request.session['wid'])
        box = Box.objects.get(box_id=box_id)
        data = {'title': 'Kolabria - Viewing Wall %s' % wall.box_id,
                'wall': wall,
                'box': box, }
        return render_to_response('walls/newwall.html', data, 
                                  context_instance=RequestContext(request))


def reset(request, bid):
    box = Box.objects.get(id=bid)
    wid = box.active_wall
    old_wall = Wall.objects.get(id=wid)
    company = old_wall.company
    old_wall.delete()
    new_wall = Wall.objects.create(company=company, box_id=bid)
    new_wall.save()
    new_wid = str(new_wall.id)
    box.active_wall = new_wid
    box.save()
    return HttpResponseRedirect('/walls/%s' % new_wid)


def unshare_box(request, box_id, shared_id):
    profile = UserProfile.objects.get(user=request.user)
    box = Box.objects.get(box_id=box_id)
    box.sharing.remove(shared_id)
    box.save()
    shared_box = Box.objects.get(box_id=shared_id)
#    msg = 'Successfully removed appliance: %s %s %s' % (shared_box.id,
#                                                        shared_box.box_id,
#                                                        shared_box.box_name)
#    messages.success(request, msg)
    return HttpResponseRedirect('/devices/edit/%s/' % box.box_id)


@login_required
def remove_box(request, box_id):
    info = """user: %s | username: %s |  company: %s | box: %s | box_name: %s"""
    profile = UserProfile.objects.get(user=request.user)
    box = Box.objects.get(box_id=box_id)
    msg0 = info % (request.user, request.user.username, 
                   profile.company, box.box_id, box.box_name)
    messages.info(request, msg0)
    box.delete()
    msg1 = 'Successfully removed appliance: %s %s %s' % (box.id,
                                                         box.box_id,
                                                         box.box_name)

    messages.success(request, msg1)
    return HttpResponseRedirect('/devices/edit/%s/' % box_id)


def auth_box(request):
    user_agent = request.META['HTTP_USER_AGENT']
    data = {'title': 'Kolabria - Valid Appliance ',}
    if user_agent[:3] == 'WWA' or 'wwa':
        box_id = user_agent
        try:
            box = Box.objects.get(box_id__iexact=box_id)
            wid = box.active_wall
            wall = Wall.objects.get(id=wid)
            request.session['auth'] = True
            request.session['wid'] = wid
            msg = "Recognized Appliance: %s id=%s" % (box.box_name, box_id)
            messages.success(request, msg)
            return HttpResponseRedirect('/wikiwall/%s' % box.box_id)
#            return HttpResponseRedirect('/walls/%s/' % wid)
        except Box.DoesNotExist:
            messages.error(request, 'Appliance %s not recognized' % box_id)
            return HttpResponseRedirect('/')
    messages.error(request, 'Access to url /box/ Unauthorized')
    return HttpResponseRedirect('/')


def the_box(request, bid):
    unsub_form = UnsubWallForm()
    pub_form = PubWallForm()
    box = Box.objects.get(id=bid)
    box_name = box.box_name
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
