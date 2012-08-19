# Create your views here.
from django.views.generic.base import TemplateView
from django.db.models import Max
from django.contrib.auth.models import User

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
