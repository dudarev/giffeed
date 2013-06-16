from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from django.views.generic import TemplateView
# AD: TODO: not good practice in accordance with PEP8.
# Mention what function and classes used in the code explicitly.
from TwitterSearch import *
from giffeed import settings, twitter


def search_form(request):
    return render(request, 'search_form.html')


def extract_urls(tweets):
    """
    takes tweets and returns a list of urls that contain gifs
    """
    extracted_urls = []
    results_count = 0  # result is something that contains a gif
    tweet_count = 0  # tweets in general
    message = ''
    for tweet in tweets:
        if 'entities' in tweet:
            if 'urls' in tweet['entities'] and tweet['entities']['urls'] != []:
                for element in tweet['entities']['urls']:
                    if element['expanded_url'].lower().endswith('.gif'):
                        if element['expanded_url'] not in extracted_urls:
                            extracted_urls.append(element['expanded_url'])
                            results_count += 1
        tweet_count += 1
        if tweet_count > (settings.total_tweets_max - 1):
            message += "Number of tweets: {} Number of results with gifs: {}".format(
                tweet_count, results_count)
            break
        else:
            print len(extracted_urls)
    return extracted_urls


def search(request):
    """

    :param request:
    :return:
    """
    if 'q' in request.GET:
        # AD: NOTE: let's also tweets that have the keyword and a word
        # `gif` in them
        search_request = (request.GET['q'] + " gif").lower()
        try:
            tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
            tso.setKeywords([search_request])  # define search request
            tso.setCount(settings.tweets_per_page)  # only give results_per_page
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
            found_urls = []
            while True:
                found_urls += extract_urls(tweets)
                if len(found_urls) >= 50:
                    break
                else:
                    tweets = ts.searchNextResults()

            context = RequestContext(request)
            context['found_urls'] = found_urls
            context['search_request'] = search_request

            return render_to_response('search_results.html',
                                      context_instance=context)

        except TwitterSearchException, e:  # to take care of errors
            message = e.message
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)


class SearchResultsView(TemplateView):
    template_name = "search_results.html"
