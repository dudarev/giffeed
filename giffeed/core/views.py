# Create your views here.
from django.views.generic.base import TemplateView

from giffeed.core.models import Post

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.all()[:5]
        return context
