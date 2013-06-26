from django.http import HttpResponseRedirect
from django.shortcuts import render
from giffeed.upload.forms import UploadForm
from giffeed.core.models import Post, Tag


def upload(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UploadForm(request.POST) # A form bound to the POST data
        info = ''
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            url = form.cleaned_data['url']
            tags = form.cleaned_data['tags'].split()
            comment = form.cleaned_data['comment']
            p = Post(user=request.user, gif_url=url, comment=comment)
            p.save()

            for tag in tags:
                p.tags.create(tag=tag)
            print(p)
            return HttpResponseRedirect('/thanks/')
    else:
        form = UploadForm()  # An unbound form

    return render(request, 'upload_form.html', {
        'form': form,
    })
