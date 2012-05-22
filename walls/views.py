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
#walls             url(r'^walls/$', views.walls), 
#create            url(r'^walls/create/$', views.create_wall),
#view              url(r'^walls/share/(?P<wid>\w+)/$', views.share_wall),
#update_sharing    #
#share             url(r'^walls/unpublish/(?P<wid>\w+)/$', views.unshare_wall),
#unshare           url(r'^walls/unshare/(?P<wid>\w+)/$', views.unshare_wall),
#update            url(r'^walls/update/(?P<wid>\w+)/$', views.update_wall),
#delete_wall       url(r'^walls/delete/(?P<wid>\w+)/$', views.delete_wall),


@login_required
def create(request):
    form = NewWallForm(request.POST or None)
    form.fields['name'].label = 'Enter WikiWall Name'
    form.fields['invited'].label = 'Invite users by email'

    if form.is_valid():
        wall = Wall.objects.create(owner=request.user,
                                   name=request.POST['name'])
        wall.save()
        wid = wall.id
        name = wall.name

        invited_emails = request.POST.get('invited', '')
        if invited_emails:
            invited_list = invited_emails.split(',')
            clean_emails = [ email.strip() for email in invited_list ]
            for email in clean_emails:
                try:
                    real = User.objects.get(email=email)
                    if email not in wall.sharing:
                        wall.sharing.append(email)
                    else:
                        messages.warning(request, '%s is already sharing' % email)
                except User.DoesNotExist:
                    messages.warning(request, 'Error: no account found for %s. Not invited')
                messages.info(request, 'Successfully added: %s' % email)


        if request.POST.getlist('publish'):
            # update wall.published model
            wall.published = request.POST.getlist('publish')
            wall.save()
            pub_msg = 'wall.published: %s' % wall.published
            messages.success(request, pub_msg)
            boxes = [ Box.objects.get(id=box) for box in wall.published ]
            messages.info(request, 'Boxes: %s' % boxes)
            for box in boxes:
                box_msg = 'box.name: %s | box.walls: %s | ' % (box.name, box.walls)
                box_msg += 'wall.name: %s | wall.id: %s' %  (wall.name,
                        wall.id)
                messages.info(request, box_msg)
                box.walls.append(str(wall.id))
                box.save()
                box_pub_msg = 'updated box.published to: %s for box.name: %s' % \
                                                            (box.walls, box.name)

        messages.success(request, 'Successfully created Wall: %s - %s' % \
                                                              (wid, name))
        return HttpResponseRedirect('/walls/')

    data = {'title': 'Kolabria - Create a new WikiWall',
            'form': form }
    return render_to_response('walls/create.html', data,
                              context_instance=RequestContext(request))


@login_required
def delete(request, wid):
    del_wall = Wall.objects.get(id=wid)
    del_form = DeleteWallForm(request.POST or None)
    del_form.fields['confirmed'].label = 'Confirm WikiWall Deletion'
    
    if del_form.is_valid():
        confirmed = request.POST.get('confirmed')
        del_wall_name = del_wall.name
        del_wall.delete()
        messages.info(request, 'Test Confirmed: Confirmed=%s for Wall Name: %s' % \
                                                            (confirmed, del_wall_name))
        messages.success(request, 'Successfully deleted WikiWall - %s' % del_wall_name)
        return HttpResponseRedirect('/walls/')
    
    data = {'title': 'Kolabria - Delete Board Confirmation',
            'del_wall': del_wall,
            'del_form': del_form,}
    return render_to_response('walls/delete.html', data,
                              context_instance=RequestContext(request))


@login_required
def walls(request):
    # Generate New Wall Form logic but hide form behind modal
    new_form = NewWallForm()
    new_form.fields['name'].label = 'Enter WikiWall Name'
    invited_label = 'Invite users by email address separate by commas.'
    new_form.fields['invited'].label = invited_label

    del_form = DeleteWallForm()
    del_form.fields['confirmed'].label = ''
    del_form.initial['confirmed'] = True

    own = Wall.objects.filter(owner=request.user)
    shared = Wall.objects.filter(sharing=request.user.email)
    walls = {'own': own, 'shared': shared,}

    data = {'title': 'Kolabria - WikiWall Dashboard', 
            'walls': walls, 
            'new_form': new_form,
            'del_form': del_form, }

    return render_to_response('walls/mywalls.html', data,
                              context_instance=RequestContext(request))

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



def reset_wall(request, wid):
    wall = Wall.objects.get(id=wid)
    wall.delete()
    msg = 'Successfully reset appliance'
    messages.success(request, msg)
    return HttpResponseRedirect('/box/')


"""
def wikiwall(request, box_id):
    ipdb.set_trace() 
    box = Box.objects.get(box_id=box_id)
    wid = box.active_wall
    wall = Wall.objects.get(id=wid)
    data = ('title': 'Kolabria - WikiWall',
            'box': box,
            'wall': wall, }
    return render_to_response('walls/wikiwall.html', data,
                              context_instance=RequestContext(request)
"""
