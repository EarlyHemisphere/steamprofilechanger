from gevent import monkey
monkey.patch_all(thread=False)

from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import json
import random
import os
import shutil
import time
import requests
from steam import SteamClient

client = SteamClient()
client.cli_login()
client.verbose_debug = True;

def GetCookies():
    client.get_web_session()
    webCookies = client.get_web_session_cookies()
    if webCookies == None:
        return "what the fuck"
    return {"steamLogin": webCookies.get("steamLogin"),
            "steamLoginSecure": webCookies.get("steamLoginSecure"),
            "sessionid": str(client.session_id),
            "steamid": str(client.steam_id)}

cookies = GetCookies()
STEAM_ID = cookies.get("steamid")
del cookies["steamid"]
wordsUrl = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
txt = urlopen(wordsUrl).read()
WORDS = txt.splitlines()

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
url = 'https://steamcommunity.com/actions/FileUploader'

data = {"sessionid": cookies.get("sessionid"),
        "doSub": "1"}

DIR = os.getcwd() + "/images/test.jpg"
sleepTime = int(input("Enter time interval: "))

try:
    while True:
        searchQuery = str(random.choice(WORDS))
        searchQuery = searchQuery[2:len(searchQuery)-1]

        imageResultNum = random.randint(0,5)
        googleUrl = "https://www.google.co.in/search?q=" + searchQuery + "&source=lnms&tbm=isch"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = BeautifulSoup(urlopen(Request(googleUrl,headers=header)), 'html.parser')
        ActualImages=[]
        imageResultCounter = 0
        
        for a in soup.find_all("div",{"class":"rg_meta"}):
            if imageResultCounter <= imageResultNum:
                link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
                ActualImages.append((link,Type))
                imageResultCounter += 1
                
        for i,(img,Type) in enumerate(ActualImages[:imageResultNum]):
            try:
                raw_img = requests.get(img,stream=True)
                with open(DIR, 'wb') as out_file:
                    shutil.copyfileobj(raw_img.raw, out_file)
            except Exception as e:
                print("could not load: " + img)
                print(e)
        
        image = open('images/test.jpg','rb')
        params = {'type': 'player_avatar_image', 'sId': STEAM_ID}
        r = requests.post(url=url,params=params,files={'avatar':image},data=data,cookies=cookies)
        print(str(r) + " for: " + searchQuery)
        time.sleep(sleepTime)
except (KeyboardInterrupt, SystemExit):
    client.logout()
    client.disconnect()
