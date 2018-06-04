import urllib
from urllib.request import urlopen
from urllib.request import Request
import urllib.error
from bs4 import BeautifulSoup
import json
import random
import os
import shutil
import http.cookies
import re
import time
import requests

wordsUrl = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
txt = urlopen(wordsUrl).read()
WORDS = txt.splitlines()

url = 'https://steamcommunity.com/actions/FileUploader'

cookies = {'steamLogin': '',
           'steamLoginSecure': '',
           'sessionid': ''}

data = {"sessionid": "",
        "doSub": "1"}

DIR = "C:/.../folderwithscript/images/test.jpg"

delay = 300

while True:
    searchQuery = str(random.choice(WORDS))
    searchQuery = searchQuery[2:len(searchQuery)-1]

    imageResultNum = random.randint(0,5)

    googleUrl = "https://www.google.co.in/search?q="+searchQuery+"&source=lnms&tbm=isch"
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
    r = requests.post(url=url,params={'type':'player_avatar_image','sId':''},files={'avatar':image},data=data,cookies=cookies)
    print(r)
    time.sleep(delay)
