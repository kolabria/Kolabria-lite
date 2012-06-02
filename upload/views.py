from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from forms import UploadFileForm

import ipdb


def handle_uploaded_file(file_obj, file_name):
    ipdb.set_trace()
    destination = open('/media/' + file_name, 'wb+')
    for chunk in file_obj.chunks():
        destination.write(chunk)
    destination.close()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.POST['title']
            handle_uploaded_file(request.FILES['file'], file_name)
            return HttpResponseRedirect('/uploaded/')
    else:
        form = UploadFileForm()
    data = {'title': 'Kolabria - Upload Form', 'form': form, }
    return render_to_response('upload/upload.html', data,
                              context_instance=RequestContext(request))


def uploaded(request):
    data = {'title': 'Kolabria - Upload Success!!'}

    return render_to_response('upload/uploaded.html', data,
                              context_instance=RequestContext(request))
