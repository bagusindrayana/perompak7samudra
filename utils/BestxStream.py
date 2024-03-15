import requests
from bs4 import BeautifulSoup
import re
import os

class BestxStream():

    def getSource(self, url):
        html = self.request(url)
        # save html to file
        # with open("test.html", "w") as f:
        #     f.write(html)
        jscripts = self.findJScripts(html)
        return jscripts[0]

    def request(self, url):
        # get host from url
        host = url.split("/")[2]
        # add header referer
        headers = {
            "Referer": f"https://{host}/",
            "Host": host,
            "sec-ch-ua" : '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile" : "?0",
            "sec-ch-ua-platform" : '"Linux"',
            "Sec-Fetch-Dest" : "iframe",
            "Sec-Fetch-Mode" : "navigate",
            "Sec-Fetch-Site" : "cross-site",
            "Sec-GPC" : "1",
            "Upgrade-Insecure-Requests" : "1",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        # get response
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    
    def findJScripts(self, html):
        soup = BeautifulSoup(html, "html.parser")
        # find script
        scripts = soup.find_all("script")
        # get value inside JScripts = '...' with regex
        jscripts = []
        for script in scripts:
            print(script.text)
            jscript = re.findall(r"JScripts = '(.*?)'", script.text)
            if jscript:
                jscripts.append(jscript[0])
        return jscripts
        