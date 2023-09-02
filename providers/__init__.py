from . import PusatFilm
from . import Muvi

class Provider(object):
    def __init__(self, **kwargs):
        self.providers = [
            PusatFilm.PusatFilm(),
            Muvi.Muvi()
        ]

    def search(self, query):
        results = []
        for provider in self.providers:
            results += provider.search(query)
        results = sorted(result, key=lambda k: k["title"])
        return results
    
    def get(self, link,providerName):
        results = {}
        for provider in self.providers:
            if provider.__class__.__name__ == providerName:
                results = provider.get(link)
                break
        return results