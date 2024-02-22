import requests, json, base64
from bs4 import BeautifulSoup


class OppaDrama(object):
    servers = ["http://oppadrama.biz"]
    sandbox = "allow-scripts allow-same-origin"

    def search(self, query,page=1,server=0):
        result = []
        url = self.servers[server]
        if int(page) > 1:
            _url = f"{url}/page/{page}?s={query}"
        else:
            _url = f"{url}?s={query}"
        try:
            r = requests.get(_url, verify=False)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            # get all article inside div.listupd
            parent = soup.find("div", class_="listupd")
            
            articles = parent.find_all("article", class_="bs")
            for article in articles:
                title = article.find("h2").text.strip().rstrip()
                link = article.find("a")["href"]
                thumb = article.find("img")["src"]
                result.append(
                    {
                        "link": "/api/get?link=" + link + "&provider=OppaDrama",
                        "detail": "/detail-series?detail="
                        + base64.b64encode(
                            json.dumps({"link": link, "provider": "OppaDrama"}).encode()
                        ).decode("utf-8"),
                        "title": title.strip().rstrip(),
                        "thumb": thumb,
                    }
                )
        except Exception as e:
            print(f"error on {_url} : " + str(e))
        return result
    def get(self, url):
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find("h1", class_="entry-title").text
        result = []
        eplister = soup.find("div", class_="eplister")
        is_episode =  eplister != None
        episodeLinks = []
        if is_episode:
            lis = eplister.find_all("li")
            for li in lis:
                link = li.find("a")["href"]
                title = li.find("div",class_="epl-title").text
                episodeLinks.append(
                    {
                        "link": "/api/get?link=" + link + "&provider=OppaDrama",
                        "detail": "/detail?detail="
                        + base64.b64encode(
                            json.dumps({"link": link, "provider": "OppaDrama"}).encode()
                        ).decode("utf-8"),
                        "title": title.strip().rstrip(),
                    }
                )
            result = {
                "title": title.strip().rstrip(),
                "episode": episodeLinks,
            }
        else:
            selectMirror = soup.find("select", class_="mirror")
            mirrors = selectMirror.find_all("option")
            streamLinks = []
            for mirror in mirrors:
                link = mirror["value"]
                if link != "":
                    _raw = base64.b64decode(link).decode("utf-8")
                    # get value inside src in _raw string
                    _soup = BeautifulSoup("<p>"+_raw+"</p>", "html.parser")
                    _iframe = _soup.find("p").find("iframe")
                    if _iframe != None:
                        _raw = _iframe["src"]
                        _url = base64.b64encode(_raw.encode()).decode("utf-8")
                        streamLinks.append({
                            "link": _raw,
                            "detail": None, 
                            "title": mirror.text.strip().rstrip()
                        })
            
            downloadLinks = []
            dlbox = soup.find("div", class_="dlbox")
            lis = dlbox.find_all("li")
            for li in lis:
                d_title = li.find("span", class_="q")
                d_link = li.find("a")
                if d_link != None:
                    downloadLinks.append({
                        "link": d_link["href"],
                        "title": d_title.text
                    })
                    

            result = {
                "title": title.strip().rstrip(),
                "stream": streamLinks,
                "download": downloadLinks,
            }

        
        return result
