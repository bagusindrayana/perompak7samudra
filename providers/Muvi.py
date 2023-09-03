import requests, json, base64
from bs4 import BeautifulSoup


class Muvi(object):
    servers = ["http://128.199.130.38"]
    sandbox = None

    def search(self, query):
        result = []
        for url in self.servers:
            _url = f"{url}?s={query}"
            try:
                r = requests.get(_url, verify=False)
                r.raise_for_status()
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
                            "title": title.strip().rstrip(),
                            "thumb": thumb,
                        }
                    )
            except Exception as e:
                print(f"error on {_url} : " + str(e))
                pass
        return result
    def get(self, url):
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        # find a.btn-01
        btn1 = soup.find("a", class_="btn-01")
        streamLink = btn1["href"].replace("https://href.li/?","")
        btn2 = soup.find("a", class_="btn-02")
        downloadLink = btn2["href"].replace("https://href.li/?","")
        # find title in meta with itemprop="name"
        title = soup.find("meta", itemprop="name")["content"]
        _url = base64.b64encode(streamLink.encode()).decode("utf-8")
        result = {
            "title": title.strip().rstrip(),
            "stream": [{"link": streamLink,"detail": "/iframe?link=" + _url + "&provider=Muvi", "title": "Stream"}],
            "download": [{"link": downloadLink, "title": "Download"}],
        }
        return result
