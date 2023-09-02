import requests, json, base64
from bs4 import BeautifulSoup


class PusatFilm(object):
    servers = ["https://51.79.193.133"]

    def search(self, query):
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
        result = []
        for url in self.servers:
            _url = f"{url}/wp-admin/admin-ajax.php?action=muvipro_core_ajax_search_movie&query={query}"
            r = requests.get(_url, headers=headers, verify=False)

            try:
                text = r.text.replace("\n", "")
                print(text)
                jsonData = json.loads(text)

                for data in jsonData["suggestions"]:
                    result.append(
                        {
                            "link": "/api/get?link=" + data["url"] + "&provider=PusatFilm",
                            "detail": "/detail?detail="+base64.b64encode(json.dumps({"link": data["url"], "provider": "PusatFilm"}).encode()).decode("utf-8"),
                            "title": data["value"],
                            "thumb": data["thumb"],
                        }
                    )
                return result
            except Exception as e:
                print(f"error on {url} : " + str(e))
                pass
        # order result by title
        result = sorted(result, key=lambda k: k["title"])
        return result

    def get(self, url):
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
            _url = base64.b64decode(link["data-frame"]).decode('utf-8')
            if "uplayer" in _url:
                _url += "&r="+_r.decode('utf-8')
            _url = base64.b64encode(_url.encode()).decode('utf-8')
            streamLinks.append({"link": "/iframe?link="+_url, "title": link.text})

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
        new_url = new_url.replace("https://kotakajaib.me/","")
        file_id = new_url.split("/")[1]
        r_download = requests.request("GET", "https://kotakajaib.me/api/"+new_url+"/download", headers=headers)
        r_download_json = r_download.json()
        downloadLinks = []
        for link in r_download_json["result"]["mirrors"]:
            downloadLinks.append({"link": "https://kotakajaib.me/mirror/"+link["server"]+"/"+file_id, "title": link["server"]})
        result = {"title":title,"stream": streamLinks, "download": downloadLinks}
        return result
