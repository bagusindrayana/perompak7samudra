from . import PusatFilm
from . import Muvi

class Provider(object):
    def __init__(self, **kwargs):
        self.providers = [
            PusatFilm.PusatFilm(),
            Muvi.Muvi()
        ]

    def listProviders(self):
        return [provider.__class__.__name__ for provider in self.providers]

    def search(self, query, **kwargs):
        results = []
        providers = kwargs.get("providers", None)
        if providers:
            for provider in self.providers:
                if provider.__class__.__name__ in providers:
                    results += provider.search(query)
        else:
            for provider in self.providers:
                results += provider.search(query)
        return results
    
    def get(self, link,providerName):
        results = {}
        for provider in self.providers:
            if provider.__class__.__name__ == providerName:
                results = provider.get(link)
                break
        return results
    
    def findProvider(self,providerName):
        for provider in self.providers:
            if provider.__class__.__name__ == providerName:
                return provider
        return None