from django.shortcuts import render
from django.http import HttpResponse
# AD: TODO: not good practice in accordance with PEP8. Mention what function and classes used in the code explicitly.
from TwitterSearch import *
from giffeed import settings


def search_form(request):
    return render(request, 'search_form.html')


def search(request):
    if 'q' in request.GET:
        # AD: NOTE: let's also tweets that have the keyword and a word `gif` in them
        search_request = (request.GET['q']+" gif").lower()
        try:
            tso = TwitterSearchOrder() # create a TwitterSearchOrder object
            tso.setKeywords([search_request]) # let's define all words we would like to have a look for
            # AD: TODO: move this to settings
            tweets_per_page = 50
            tso.setCount(tweets_per_page) # please dear Mr Twitter, only give us results_per_page results per page
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
            results_count = 0  # result is something that contains a gif
            tweet_count = 0  # tweets in general
            # AD: TODO: move to settings (?), maximum number of tweets to get 
            # it may be larger than tweets_per_page
            total_tweets_max = tweets_per_page
            message = ''

            for tweet in ts.searchTweetsIterable(tso):  # this is where the fun actually starts :)
                if 'entities' in tweet:
                     if 'urls' in tweet['entities'] and tweet['entities']['urls'] != []:
                         for element in tweet['entities']['urls']:
                             print element['expanded_url']
                             if element['expanded_url'].lower().endswith('.gif'):
                                 if element['expanded_url'] not in found_urls:
                                     info += '<img src="{}">'.format(element['expanded_url'])
                                     found_urls.append(element['expanded_url'])
                                     results_count += 1
                tweet_count += 1
                if tweet_count > (total_tweets_max - 1):
                    message += "Number of tweets: {} Number of results with gifs: {}".format(
                        tweet_count, results_count)
                    break
            else:
                # AD: TODO: this is probably should be removed, it is here now for debugging
                if tweet_count == 0:
                    message = "Zero tweets were found."
                else:
                    message = "Number of tweets: {} Number of results with gifs: {}".format(
                        tweet_count, results_count)
            print len(found_urls)
            # AD: TODO: do this with template
            html = "<html><body><ul>{}</ul><p>{}</p></body></html>".format(info, message)
            return HttpResponse(html)

        except TwitterSearchException, e: # take care of all those ugly errors if there are some
            message = e.message
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
