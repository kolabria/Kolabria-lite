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


# Legend of urls and views
#create            url(r'^walls/create/$', views.create_wall),
#view              url(r'^walls/share/(?P<wid>\w+)/$', views.share_wall),
#update_sharing    #
#share             url(r'^walls/unpublish/(?P<wid>\w+)/$', views.unshare_wall),
#unshare           url(r'^walls/unshare/(?P<wid>\w+)/$', views.unshare_wall),
#update            url(r'^walls/update/(?P<wid>\w+)/$', views.update_wall),
#delete_wall       url(r'^walls/delete/(?P<wid>\w+)/$', views.delete_wall),


def view(request, wid):
    # Get a specific wall by Mongo object id
    wall = Wall.objects.get(id=wid)
    box_id = wall.box_id
    box = Box.objects.get(box_id=box_id)
    data = {'title': 'Kolabria - Viewing Wall %s' % wall.box_id,
            'wall': wall,
            'box': box, }
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
    return render_to_response('walls/initiator-wall.html', data, 
                              context_instance=RequestContext(request))

def view_slave_box(request, wid):
    # Appliance view for slave appliance. Viewing master appliance wall
    wall = Wall.objects.get(id=wid)
    box_id = wall.box_id
    box = Box.objects.get(box_id=box_id)
    data = {'title': 'Kolabria - Viewing Wall %s' % wall.box_id,
            'wall': wall,
            'box': box, }
    return render_to_response('walls/initiator-wall.html', data, 
                              context_instance=RequestContext(request))



def reset_box(request, box_id):
    """
    To be called from initiating Device.
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
    return HttpResponseRedirect('/box/')


def restore_receiver_box(request, box_id):
    ipdb.set_trace()
    box = Box.objects.get(box_id=box_id)
    wid = box.active_wall
    wall = Wall.objects.get(id=wid)
    wall.delete()

    msg = 'Successfully reset appliance'
    messages.success(request, msg)
    return HttpResponseRedirect('/box/')


def quit_box(request, box_id):
    ipdb.set_trace()
    box = Box.objects.get(box_id=box_id)
    wid = box.active_wall
    wall = Wall.objects.get(id=wid)
    wall.delete()
    return HttpResponseRedirect('/thank-you/')


def thank_you(request):
    data = {'title': 'Kolabria - Session Complete - Feedback Form',
           }
    return render_to_response('walls/thank-you.html', data,
                              context_instance=RequestContext(request))
