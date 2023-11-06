import requests, json, base64
from bs4 import BeautifulSoup


class Idlix(object):
    servers = ["https://tv.idlixplus.net"]
    sandbox = "allow-scripts allow-same-origin"

    def search(self, query,page=1,server=0):
        headers = {
            "authority": "51.79.193.133",
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://tv.idlixplus.net/",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        result = []
        url = self.servers[server]
        _url = f"{url}/search/{query}/page/{page}"
        
        try:
            r = requests.get(_url, headers=headers, verify=False)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            # get article tag inside div#gmr-main-load
            articles = soup.find("div", {"class": "search-page"}).find_all("article")
            for article in articles:
                title = article.find("div", {"class": "title"}).text
                thumb = article.find("img", {})["src"]
                link = article.find("a", {})["href"]
                detailLink = base64.b64encode(
                    json.dumps({"link": link, "provider": "PusatFilm"}).encode()
                ).decode("utf-8")
                if "/season/" in link:
                    detailLink = "/detail-series?detail=" + detailLink
                else:
                    detailLink = "/detail?detail=" + detailLink
                result.append(
                    {
                        "link": "/api/get?link=" + link + "&provider=PusatFilm",
                        "detail": detailLink,
                        "title": title.strip().rstrip(),
                        "thumb": thumb,
                    }
                )
        except Exception as e:
            print(f"error on {_url} : " + str(e))
        return result

    def get(self, url):
        if "/tv/" in url:
            return self.getSeries(url)
        else:
            return self.getMovies(url)

    def getMovies(self, url):
        headers = {
            "authority": "51.79.193.133",
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://51.79.193.133/",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        r = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        # get iframe src inside div.gmr-embed-responsive
        iframeSrc = soup.find("div", {"class": "gmr-embed-responsive"}).find("iframe")[
            "src"
        ]

        # get title from h1.entry-title
        title = soup.find("h1", {"class": "entry-title"}).text

        r_embed = requests.get(iframeSrc, headers=headers, verify=False)
        soup_embed = BeautifulSoup(r_embed.text, "html.parser")
        # get all link inside ul#dropdown-server
        links = soup_embed.find("ul", {"id": "dropdown-server"}).find_all("a")
        streamLinks = []
        for link in links:
            _r = base64.b64encode("https://51.79.193.133/".encode())
            _raw = base64.b64decode(link["data-frame"]).decode("utf-8")
            if "uplayer" in _raw:
                _raw += "&r=" + _r.decode("utf-8")
            _url = base64.b64encode(_raw.encode()).decode("utf-8")
            streamLinks.append({"link":_raw,"detail": "/iframe?link=" + _url + "&provider=PusatFilm", "title": link.text})

        new_url = iframeSrc.replace("embed", "file")
        headers = {
            "authority": "kotakajaib.me",
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": new_url,
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        new_url = new_url.replace("https://kotakajaib.me/", "")
        file_id = new_url.split("/")[1]
        r_download = requests.request(
            "GET", "https://kotakajaib.me/api/" + new_url + "/download", headers=headers
        )
        r_download_json = r_download.json()
        downloadLinks = []
        if "result" in r_download_json and r_download.status_code == 200:
            for link in r_download_json["result"]["mirrors"]:
                downloadLinks.append(
                    {
                        "link": "https://kotakajaib.me/mirror/"
                        + link["server"]
                        + "/"
                        + file_id,
                        "title": link["server"].strip().rstrip(),
                    }
                )
        result = {"title": title, "stream": streamLinks, "download": downloadLinks}
        return result

    def getSeries(self, url):
        headers = {
            "authority": "51.79.193.133",
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://51.79.193.133/",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        r = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")

        # get all link from class button s-eps
        links = soup.find_all("a", {"class": "button s-eps"})

        title = soup.find("h1", {"class": "entry-title"}).text.strip().rstrip()

        epsLinks = []
        for link in links:
            epsLinks.append(
                {
                    "link": "/api/get?link=" + link["href"] + "&provider=PusatFilm",
                    "detail": "/detail?detail="
                    + base64.b64encode(
                        json.dumps(
                            {"link": link["href"], "provider": "PusatFilm"}
                        ).encode()
                    ).decode("utf-8"),
                    "title": link.text,
                }
            )

        result = {"title": title, "episode": epsLinks}
        return result
