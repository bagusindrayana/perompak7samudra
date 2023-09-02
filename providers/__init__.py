from . import PusatFilm

class Provider(object):
    def __init__(self, **kwargs):
        self.providers = [
            PusatFilm.PusatFilm()
        ]

    def search(self, query):
        results = []
        for provider in self.providers:
            results += provider.search(query)
        return results
    
    def get(self, link,providerName):
        results = []
        for provider in self.providers:
            if provider.__class__.__name__ == providerName:
                results = provider.get(link)
                break
        return results