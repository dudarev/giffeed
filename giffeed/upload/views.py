from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from giffeed.upload.forms import UploadForm
from giffeed.core.models import Post
from django.core.urlresolvers import reverse


def upload(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = UploadForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            #  Process the data in form.cleaned_data
            # ...
            url = form.cleaned_data['url']
            tags = form.cleaned_data['tags'].split()
            comment = form.cleaned_data['comment']
            collection = Post.objects.filter(user=request.user, gif_url=url)
            if collection.exists():
                message = 'You have already posted this gif.'
                return HttpResponse(message)
            else:
                p = Post(user=request.user, gif_url=url, comment=comment)
                p.save()

            for tag in tags:
                p.tags.create(tag=tag)
            return HttpResponseRedirect(reverse('user', args=[request.user.username]))
    else:
        form = UploadForm()  # An unbound form

    return render(request, 'upload_form.html', {
        'form': form,
    })
