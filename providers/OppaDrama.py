import requests, json, base64, os
from bs4 import BeautifulSoup
import urllib.parse


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
                thumb = article.find("img")["src"].replace("?resize=246,350","")
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
                        # _url = base64.b64encode(_raw.encode()).decode("utf-8")
                        _detail = None
                        
                        if("bestx.stream" in _raw):
                            BASE_URL = os.environ.get('BASE_URL')
                            _detail = BASE_URL+"/stream-decrypt/bestx-stream?target="+_raw
                        elif("vidhidepro" in _raw):
                            BASE_URL = os.environ.get('BASE_URL')
                            referer = url.split("/")[2]
                            _detail = BASE_URL+"/stream-decrypt/vidhidepro?target="+_raw+"&referer="+url.split("/")[0]+"//"+referer+"/"
                        streamLinks.append({
                            "link": _raw,
                            "detail": _detail, 
                            "title": mirror.text.strip().rstrip()
                        })
            
            downloadLinks = []
            dlbox = soup.find("div", class_="dlbox")
            if dlbox != None:
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
    

    def convertLink(self,link,host):
        streamLink = None
        if("bestx.stream" in host):
            streamHost = link.split("/")[2]
            # add header referer
            headers = {
                'Origin': f'https://{host}',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': f'https://{host}/',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'sec-gpc': '1',
                'Host': streamHost,
                'Keep-Alive': 'keep-alive',
                'accept': '*/*',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'sec-ch-ua-platform': '"Linux"',
                'sec-ch-ua-mobile': '?0',
                'Accept-Language': 'en-US,en'
            }



            proxy_url = os.environ.get('M3U8_PROXY')
            url = link
            url = urllib.parse.quote(link)
            streamLink = proxy_url+"?url="+url+"&headers="+json.dumps(headers)
        else:
            proxy_url = os.environ.get('M3U8_PROXY')
            url = link
            url = urllib.parse.quote(link)
            streamHost = link.split("/")[2]
            headers = {
                'Origin': f'https://{host}',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': f'https://{host}/',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'sec-gpc': '1',
                'Host': streamHost,
                'Keep-Alive': 'keep-alive',
                'accept': '*/*',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-mobile': '?0',
                'Accept-Language': 'en-US,en'
            }
            streamLink = proxy_url+"?url="+url+"&headers="+json.dumps(headers)
        return {
            "stream":streamLink,
            "subtitle":""
        }