from . import PusatFilm
from . import Muvi
from . import OppaDrama

class Provider(object):
    def __init__(self, **kwargs):
        self.providers = [
            PusatFilm.PusatFilm(),
            Muvi.Muvi(),
            OppaDrama.OppaDrama(),
        ]

    def listProviders(self):
        return [provider.__class__.__name__ for provider in self.providers]

    def search(self, query, **kwargs):
        results = []
        providers = kwargs.get("providers", None)
        page = kwargs.get("page", 1)
        if providers:
            for provider in self.providers:
                if provider.__class__.__name__ in providers:
                    results += provider.search(query,page)
        else:
            for provider in self.providers:
                results += provider.search(query,page)
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