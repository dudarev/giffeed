from django.shortcuts import render
from django.http import HttpResponse
from TwitterSearch import *
from giffeed import settings


def search_form(request):
    return render(request, 'search_form.html')


def search(request):
    if 'q' in request.GET:
        search_request = (request.GET['q']+".gif").lower()
        try:
            tso = TwitterSearchOrder() # create a TwitterSearchOrder object
            tso.setKeywords([search_request]) # let's define all words we would like to have a look for
            tso.setCount(10) # please dear Mr Twitter, only give us 10 results per page
            tso.setIncludeEntities(True) # and don't give us all those entity information

            # it's about time to create a TwitterSearch object with our secret tokens
            ts = TwitterSearch(
                consumer_key = settings.TWITTER_CONSUMER_KEY,
                consumer_secret = settings.TWITTER_CONSUMER_SECRET,
                access_token = settings.TWITTER_ACCESS_TOKEN,
                access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
             )

            ts.authenticate() # we need to use the oauth authentication first to be able to sign messages

            found_urls = []
            info = ''
            for tweet in ts.searchTweetsIterable(tso):# this is where the fun actually starts :)
                 if 'entities' in tweet:
                     if 'urls' in tweet['entities'] and tweet['entities']['urls'] != []:
                         for element in tweet['entities']['urls']:
                             if element['expanded_url'].lower().endswith(search_request):
                                 if element['expanded_url'] not in found_urls:
                                     info += '<img src="{}">'.format(element['expanded_url'])
                                     found_urls.append(element['expanded_url'])
            print (found_urls)
            html = "<html><body><ul>{}</ul></body></html>".format(info)
            return HttpResponse(html)

        except TwitterSearchException, e: # take care of all those ugly errors if there are some
            message = e.message
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
