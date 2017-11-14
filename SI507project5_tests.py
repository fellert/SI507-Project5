import unittest
from SI507project5_code import *

class TestTumblrAPI(unittest.TestCase):
    # Creates one API call - similar to the one in SI507project5_code.py
    def setUp(self):
        self.test_url = "https://api.tumblr.com/v2/blog/{0}/posts".format('rollingstone.tumblr.com')
        self.test_params = {'limit': 30, 'tag': 'Led Zeppelin'}
        self.test_posts = get_data_from_api(self.test_url,"Tumblr",self.test_params)
        self.cache = CACHE_DICTION
        self.creds = CREDS_DICTION
        self.now = datetime.now()
        self.format = DATETIME_FORMAT

    # Tests if the length of each request matches the parameter submitted.
    def test_len(self):
        self.assertEqual(len(self.test_posts['response']['posts']), self.test_params['limit'],
                            'Did not return right amount of posts.')

    # For the Rolling Stone request, checks if each post has the tag parameter submitted ('Led Zeppelin').
    def test_tags(self):
        posts = self.test_posts['response']['posts']
        for post in posts:
            self.assertIn(self.test_params['tag'], post['tags'], 'Tag not here.')

    # Tests if the cache files contains the correct request urls that were initialized above.
    def test_cache_url(self):
        requests = list(self.cache.keys())
        test_request = create_request_identifier(self.test_url,self.test_params)
        self.assertIn(test_request, requests, 'Request data not stored in cache.')

    # Tests if the creds file actually stored any of the Tumblr credentials.
    def test_credentials(self):
        credentials = get_from_cache('TUMBLR', self.creds)
        self.assertTrue(len(credentials) != 0, 'No credentials were stored.')

    # Manually checks is the timestamp in the creds file is less than 7 days old.
    def test_has_expired(self):
        timestamp = datetime.strptime(self.creds['TUMBLR']['timestamp'], self.format)
        last_pulled = (timestamp - self.now).days
        self.assertTrue(last_pulled < self.creds['TUMBLR']['expire_in_days'], 'Cache outdated.')

    # Resets several variables to None. I tried use os.remove to delete the cache and cred files
    # but ran into issues but I did not realize that tearDown runs after each method
    # (not the end of the class), which would mean that I am running an API call five times
    # in a row (for each test method).
    def tearDown(self):
        self.test_posts = None
        self.now = None
        self.cache = None
        self.creds = None
        self.test1_url = None


if __name__ == "__main__":
    unittest.main(verbosity=2)
