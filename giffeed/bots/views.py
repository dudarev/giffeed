from django.conf import settings
from django.http import HttpResponse
import datetime

from django.db import IntegrityError, connection

from giffeed.bots.models import Bot
from giffeed.core.models import Post


def update(request):

    b = Bot.objects.order_by('last_run_at')[0]
    if datetime.timedelta(hours=settings.OLDEST_LAST_RUN_DELTA) < datetime.datetime.now()-b.last_run_at:
        count_added = 0
        count_duplicates = 0
        links = b.parse_url()
        for l in reversed(links):
            p = Post(user=b.user, gif_url=l)
            try:
                p.save()
                count_added += 1
            except IntegrityError:
                connection._rollback()
                count_duplicates += 1
        b.last_run_at = datetime.datetime.now()
        b.save()
        response = "added: {0}, duplicates: {1}".format(count_added, count_duplicates)
    else:
        response = "oldest bot updated less that {0} hours ago".format(settings.OLDEST_LAST_RUN_DELTA)
    return HttpResponse(response)
