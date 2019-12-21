import unittest
from twistdl import TwistDL
from urllib.parse import urlparse


class MyTestCase1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    # Verify we get source and can decrypt them to valid URLs.
    def testCreds(self):
        client = TwistDL()
        animes = client.search_animes(title='made in abyss')
        if not animes:
            exit(1)
        for anime in animes:
            for episode in anime.episodes:
                if client.base_url in episode.url and urlparse(episode.url):
                    continue
        return
