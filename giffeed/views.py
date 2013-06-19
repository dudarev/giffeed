from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from django.views.generic import TemplateView
# AD: TODO: not good practice in accordance with PEP8.
# Mention what function and classes used in the code explicitly.
from TwitterSearch import *
from models import SearchKeyWord
from giffeed import settings, twitter
from datetime import datetime, timedelta


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
    try:
        tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
        tso.setKeywords([search_request])  # define search request
        tso.setCount(settings.tweets_per_page)  # only results_per_page
        tso.setIncludeEntities(True)  # give us entity information

        # create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key=twitter.TWITTER_CONSUMER_KEY,
            consumer_secret=twitter.TWITTER_CONSUMER_SECRET,
            access_token=twitter.TWITTER_ACCESS_TOKEN,
            access_token_secret=twitter.TWITTER_ACCESS_TOKEN_SECRET
        )

        ts.authenticate()  # user must authenticate first
        tweets = ts.searchTweetsIterable(tso)
        found_urls = extract_urls(tweets)
        search_keyword_object = SearchKeyWord()
        search_keyword_object.gifs = found_urls
        search_keyword_object.search_keyword = search_request
        search_keyword_object.updated_at = datetime.now()
        print(search_keyword_object)
        search_keyword_object.save()
        return found_urls

    except TwitterSearchException, e:  # to take care of errors
        message = e.message


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
                found_urls = fetch_tweets(search_request)
        else:
            found_urls = fetch_tweets(search_request)
        print(found_urls)
        context = RequestContext(request)
        context['found_urls'] = found_urls
        context['search_request'] = search_request

        return render_to_response('search_results.html', context_instance=context)
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)


class SearchResultsView(TemplateView):
    template_name = "search_results.html"
