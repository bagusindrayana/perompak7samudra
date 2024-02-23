import requests
from bs4 import BeautifulSoup

import base64
import json
import os
import urllib.parse



class Idlix(object):
    servers = []
    sandbox = "allow-scripts allow-same-origin"

    def checkLink(self):
        print("Check")
        _live = "https://idlixian.com"
        r = requests.get(_live,headers={
            "authority":"pusatfilm21.info",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        })
        print(f"Finish Check {r.status_code}")
        r.raise_for_status()
        self.servers.append(r.url)

    def search(self, query,page=1,server=0):
        self.checkLink()
        headers = {
            "authority": "51.79.193.133",
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://idlixian.com/",
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
                    json.dumps({"link": link, "provider": "Idlix"}).encode()
                ).decode("utf-8")
                if "/season/" in link:
                    detailLink = "/detail-series?detail=" + detailLink
                else:
                    detailLink = "/detail?detail=" + detailLink
                result.append(
                    {
                        "link": "/api/get?link=" + link + "&provider=Idlix",
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
        referer = url.split("/")[2]
        headers = {
            "authority": "51.79.193.133",
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://"+referer+"/",
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

        title = soup.find("div",class_="sheader").find("h1").text
        
        links = soup.find("ul", {"id": "playeroptionsul"}).find_all("li")
        streamLinks = []
        for link in links:
            type = link["data-type"]
            post = link["data-post"]
            nume = link["data-nume"]
            resAjax = self._ajaxAdmin("doo_player_ajax",post,nume,type)
            value_str = json.dumps(resAjax)
            urlData = urllib.parse.urlencode({"data":value_str})
            _raw = self._requestDecrypt(urlData)
            _url = base64.b64encode(_raw.encode()).decode("utf-8")
            streamLinks.append({
                "link": _raw,
                "detail": _raw, 
                "title": link.text.strip().rstrip()
            })

            
            

        # new_url = iframeSrc.replace("embed", "file")
        # headers = {
        #     "authority": "kotakajaib.me",
        #     "accept": "application/json",
        #     "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        #     "referer": new_url,
        #     "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": '"Windows"',
        #     "sec-fetch-dest": "empty",
        #     "sec-fetch-mode": "cors",
        #     "sec-fetch-site": "same-origin",
        #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        #     "x-requested-with": "XMLHttpRequest",
        # }
        # new_url = new_url.replace("https://kotakajaib.me/", "")
        # file_id = new_url.split("/")[1]
        # r_download = requests.request(
        #     "GET", "https://kotakajaib.me/api/" + new_url + "/download", headers=headers
        # )
        # r_download_json = r_download.json()
        downloadLinks = []
        # if "result" in r_download_json and r_download.status_code == 200:
        #     for link in r_download_json["result"]["mirrors"]:
        #         downloadLinks.append(
        #             {
        #                 "link": "https://kotakajaib.me/mirror/"
        #                 + link["server"]
        #                 + "/"
        #                 + file_id,
        #                 "title": link["server"].strip().rstrip(),
        #             }
        #         )
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
                    "link": "/api/get?link=" + link["href"] + "&provider=Idlix",
                    "detail": "/detail?detail="
                    + base64.b64encode(
                        json.dumps(
                            {"link": link["href"], "provider": "Idlix"}
                        ).encode()
                    ).decode("utf-8"),
                    "title": link.text,
                }
            )

        result = {"title": title, "episode": epsLinks}
        return result

    def _ajaxAdmin(self,action,post,nume,type):
        if len(self.servers) <= 0:
            self.checkLink()
        url = self.servers[0]+"/wp-admin/admin-ajax.php"

        payload = "action="+action+"&post="+post+"&nume="+nume+"&type="+type
        headers = {
            'authority': 'tv.idlixofficial.co',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': self.servers[0],
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"STATUS : {response.status_code}")
        return response.json()
    
    def _requestDecrypt(self,dataUrl):
        BASE_URL = os.environ.get('BASE_URL')
        return BASE_URL+"/idlix?"+dataUrl
        res = requests.request("GET", BASE_URL+"/idlix?"+dataUrl)
        print(res.text)
        # find #result
        soup = BeautifulSoup(res.text, "html.parser")
        result = soup.find("div", {"id": "result"}).text
        return result
    
    def convertLink(self,link):
        self.checkLink()
        last = link.split("/")[-1]
        url = "https://jeniusplay.com/player/index.php?data="+last+"&do=getVideo"

        payload = "hash=ba3c5e7b68dbdb900c4ee701df6cd6b5&r="+self.servers[0]
        headers = {
            'authority': 'jeniusplay.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://jeniusplay.com',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'fireplayer_player=r54vhpe1m2p3h5lsfvk1ked4uo'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        proxy_url = os.environ.get('M3U8_PROXY')
        streamLink = proxy_url+"?url="+response.json()['videoSource']+'&headers={"referer":"https://jeniusplay.com/","x-requested-with":"XMLHttpRequest"}'
        return streamLink

  
# eval_res, tempfile = js2py.run_file("./js/crypto.js") 
# tempfile.wish("GeeksforGeeks")