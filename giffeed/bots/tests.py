"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from giffeed.bots.models import Bot


class SimpleTest(TestCase):
    def test_url_parsing_duplicates(self):
        """
        Tests that gif links are parsed correctly without duplicates.
        """

        b = Bot(name='_test', url='http://example.com')
        links = b.parse_url(file_name='giffeed/bots/test_data/gif_parsing.txt')
        self.assertEqual(len(links), 4)

    def test_url_parsing_ignore(self):
        """
        Tests that for source 'topsy' all links that have topsy are ignored.
        """

        b = Bot(name='_test', url='http://example.com', source='topsy')
        links = b.parse_url(file_name='giffeed/bots/test_data/gif_parsing.txt')
        for l in links:
            self.assertFalse('topsy' in l)
