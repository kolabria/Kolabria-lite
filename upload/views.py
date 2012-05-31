from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.context_processors import csrf
from django.core.files import File
import settings

from forms import UploadFileForm
from models import Upload

import ipdb

def _upload(fl):
    '''Handle the actual file upload.'''
    try:
        destination = open("%s/%s" % (settings.UPLOAD_PATH, fl.name), 'wb+')
        for chunk in fl.chunks():
            print "chunk"
            destination.write(chunk)
    finally:
        uploaded_file = File(destination)
        destination.close()
        return uploaded_file


def upload_file(request):
    ipdb.set_trace()
    obj = Upload()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
    else:
        form = UploadFileForm()

    if form.is_valid():
        #_upload(request.FILES['file'])
        #u.file = _upload(request.FILES['file'])
        #u.description = form.cleaned_data['description']
        form.save(request, obj)
        return HttpResponseRedirect('/uploaded/')
    else:
        context = {}
        context.update(csrf(request))
        context.update({'form': form})
        return render_to_response('upload/upload.html', context)


def uploaded(request):
    """
    Called on successfully completed upload.
    """

    data = {'title': 'Kolabria - File upload success',
           }
    return render_to_response('upload/uploaded.html', data,
                              context_instance=RequestContext(request))
