import requests, json, base64
from bs4 import BeautifulSoup


class Muvi(object):
    servers = ["http://128.199.130.38"]

    def search(self, query):
        result = []
        for url in self.servers:
            _url = f"{url}?s={query}"
            r = requests.get(_url, verify=False)
            soup = BeautifulSoup(r.text, "html.parser")
            # get all div inside div.movies-list-full
            parent = soup.find("div", class_="movies-list-full")
            divs = parent.find_all("div", class_="ml-item")
            for div in divs:
                title = div.find("span", class_="mli-info").text
                link = div.find("a")["href"]
                thumb = div.find("img")["data-original"]
                result.append(
                    {
                        "link": "/api/get?link=" + link + "&provider=Muvi",
                        "detail": "/detail?detail="
                        + base64.b64encode(
                            json.dumps({"link": link, "provider": "Muvi"}).encode()
                        ).decode("utf-8"),
                        "title": title,
                        "thumb": thumb,
                    }
                )
        result = sorted(result, key=lambda k: k["title"])
        return result

    def get(self, url):
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        # find a.btn-01
        btn1 = soup.find("a", class_="btn-01")
        streamLink = btn1["href"].replace("https://href.li/?","")
        print(streamLink)
        btn2 = soup.find("a", class_="btn-02")
        downloadLink = btn2["href"].replace("https://href.li/?","")
        # find title in meta with itemprop="name"
        title = soup.find("meta", itemprop="name")["content"]
        result = {
            "title": title,
            "stream": [{"link": streamLink, "title": "Stream"}],
            "download": [{"link": downloadLink, "title": "Download"}],
        }
        return result
