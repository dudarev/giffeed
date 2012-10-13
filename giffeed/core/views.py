# Create your views here.
from django.views.generic.base import TemplateView
from django.db.models import Max
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

        posts_list = Post.objects.all().filter(user=u).order_by('-time_added')
        paginator = Paginator(posts_list, 10)  # Show 10 posts per page

        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        context['latest_posts'] = posts
        return context
