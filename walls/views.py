from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from mongoengine.django.auth import User

from walls.forms import NewWallForm, UpdateWallForm, DeleteWallForm
from walls.forms import ShareWallForm, UnshareWallForm
from walls.forms import PubWallForm, UnpubWallForm 
from walls.models import Wall
from appliance.models import Box

import ipdb

def view(request, wid):
    # Get a specific wall by Mongo object id
    wall = Wall.objects.get(id=wid)
    box_id = wall.box_id
    box = Box.objects.get(box_id=box_id)
    client = request.session['name']
    data = {'title': 'Kolabria - Viewing Wall %s' % wall.box_id,
            'wall': wall,
            'box': box, 
            'client' client, }
    return render_to_response('walls/newwall.html', data, 
                              context_instance=RequestContext(request))


def view_master_box(request, wid):
    # Appliance view for initiating appliance, sharing wall with slave
    wall = Wall.objects.get(id=wid)
    box_id = wall.box_id
    box = Box.objects.get(box_id=box_id)
    data = {'title': 'Kolabria - Viewing Wall %s' % wall.box_id,
            'wall': wall,
            'box': box, }
    return render_to_response('walls/master-wall.html', data, 
                              context_instance=RequestContext(request))

def view_slave_box(request, wid):
    # Appliance view for slave appliance. Viewing master appliance wall
    wall = Wall.objects.get(id=wid)
    box_id = wall.box_id
    box = Box.objects.get(box_id=box_id)
    data = {'title': 'Kolabria - Viewing Wall %s' % wall.box_id,
            'wall': wall,
            'box': box, }
    return render_to_response('walls/slave-wall.html', data, 
                              context_instance=RequestContext(request))



def reset_box(request, box_id):
    """
    To be called from Host Device.
    Flushes the currently active wall.
    Generates a new wall with a new wall.code
    """
    box = Box.objects.get(box_id=box_id)
    wid = box.active_wall
    wall = Wall.objects.get(id=wid)
    wall.delete()
    box.active_wall = ''
    new_wall = Wall.objects.create(company=box.company,
                                   box_id=box.box_id)
    new_wall.save()
    box.active_wall = str(new_wall.id)
    box.save()
    msg = 'Successfully reset appliance. New Code: %s' % new_wall.code
    messages.success(request, msg)
    return HttpResponseRedirect('/host/')


def restore_box(request, box_id):
    """
    To be called from Receiver Device.
    Restores Receiver Device to default (own) active wall.
    """
    box = Box.objects.get(box_id=box_id)
    wid = box.active_wall
    wall = Wall.objects.get(id=wid)
    wall.delete()

    msg = 'Restore appliance -- not yet implemented'
    messages.success(request, msg)
    return HttpResponseRedirect('/host/')


def thank_you(request):
    """
    Called on completed session from Client View.
    Terminates client's session without terminating other sessions.
    Returns /thank-you view with Feedback form.
    """

    data = {'title': 'Kolabria - Session Complete - Feedback Form',
           }
    return render_to_response('walls/thank-you.html', data,
                              context_instance=RequestContext(request))
