import datetime

from django.db import IntegrityError, connection

from celery.task import task

from giffeed.bots.models import Bot
from giffeed.core.models import Post

@task(ignore_result=True)
def run_bots():
    count_added = 0
    count_duplicates = 0
    b = Bot.objects.order_by('last_run_at')[0]
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
    return "added: {0}, duplicates: {1}".format(count_added, count_duplicates)
