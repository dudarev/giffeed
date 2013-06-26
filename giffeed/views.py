from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from twython import Twython
from models import SearchKeyWord
from django.conf import settings
from datetime import datetime, timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_form(request):
    return render(request, 'search_form.html')


def extract_urls (tweets):
    """
    :takes tweets and extracts urls that contain "gif"
    """

    extracted_urls = []
    tweet_count = 0  # tweets in general
    for tweet in tweets:
        if 'entities' in tweet:
            if 'urls' in tweet['entities'] and tweet['entities']['urls'] != []:
                for element in tweet['entities']['urls']:
                    if element['expanded_url'].lower().endswith('.gif'):
                        if element['expanded_url'] not in extracted_urls:
                            extracted_urls.append(element['expanded_url'])
                            tweet_count += 1
        if tweet_count > (settings.total_tweets_max - 1):
            break
    else:
        print len(extracted_urls)
    return extracted_urls


def fetch_tweets(search_request):
    """
    fetches tweets from Twitter API extracts urls and updates db
    """
    twitter = Twython(settings.TWITTER_CONSUMER_KEY,
                      settings.TWITTER_CONSUMER_SECRET,
                      settings.TWITTER_ACCESS_TOKEN,
                      settings.TWITTER_ACCESS_TOKEN_SECRET)

    tweets = twitter.search_gen(search_request)
    found_urls = extract_urls(tweets)

    search_keyword_object = SearchKeyWord()
    search_keyword_object.gifs = found_urls
    search_keyword_object.search_keyword = search_request
    search_keyword_object.updated_at = datetime.now()
    print(search_keyword_object)
    search_keyword_object.save()
    return found_urls


def search(request):
    """
    searches
    """
    if 'q' in request.GET:
        # AD: NOTE: let's also tweets that have the keyword and
        # a word `gif` in them
        search_request = (request.GET['q'] + " gif").lower()
        collection = SearchKeyWord.objects.filter(search_keyword=search_request)
        if collection.exists():
            obj = collection[0]
            if (datetime.now() - obj.updated_at) <= timedelta(hours=3):
                found_urls = obj.gifs
            else:
                obj.delete()
                found_urls = fetch_tweets(search_request)
        else:
            found_urls = fetch_tweets(search_request)
        print(found_urls)

        urls_list = found_urls
        paginator = Paginator(urls_list, 10)  # Show 10 posts per page
        page = request.GET.get('page')
        try:
            urls = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            urls = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            urls = paginator.page(paginator.num_pages)

        context = RequestContext(request)
        context['urls'] = urls
        context['search_request'] = search_request
        context['q'] = request.GET['q']

        return render_to_response('search_results.html', context_instance=context)
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
