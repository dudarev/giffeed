# Create your views here.
from django.views.generic.base import TemplateView
from django.db.models import Max
from django.contrib.auth.models import User

from giffeed.core.models import Post

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        posts = []
        for u in User.objects.annotate(last_post=Max('post__time_added')).order_by('-last_post')[:10]:
            try:
                posts.append(u.post_set.latest('time_added'))
            except:
                pass

        context['latest_posts'] = posts
        return context

class UserPageView(TemplateView):

    template_name = "user.html"

    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data(**kwargs)

        username = kwargs['username']
        context['username'] = username 

        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            context['error_message'] = "Such user does not exist."
            return context

        posts = Post.objects.all().filter(user=u).order_by('-time_added')[:10]

        context['latest_posts'] = posts
        return context
