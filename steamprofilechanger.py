import json
import random
import os
import shutil
import time
import requests
import getpass
import base64
import cryptography.hazmat.backends
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from binascii import hexlify
from cryptography.hazmat.primitives.hashes import Hash, SHA1
from PIL import Image

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
IMG_DIR = os.getcwd() + '/images/img.jpg'
STEAM_SIZE_LIMIT = 1024000

def getRSAKey(username):
    global user_agent
    url = 'https://steamcommunity.com/login/getrsakey/'
    values = {'username' : username, 'donotcache' : str(int(time.time()*1000))}
    headers = {'User-Agent' : user_agent}
    post = urlencode(values).encode('utf-8')
    req = Request(url, post, headers)
    response = urlopen(req).read()
    return json.loads(response)

def getAndEncryptPass(rsaData):
    mod = int(str(rsaData['publickey_mod']), 16)
    exp = int(str(rsaData['publickey_exp']), 16)
    rsa = RSA.construct((mod, exp))
    cipher = PKCS1_v1_5.new(rsa)
    return base64.b64encode(cipher.encrypt(getpass.getpass(prompt='Steam password: ', stream=None).encode('utf-8')))

def generateSessionID():
    backend = cryptography.hazmat.backends.default_backend()
    random_bytes = os.urandom(32)
    sha = Hash(SHA1(), backend)
    sha.update(random_bytes)
    return hexlify(sha.finalize())[:32].decode('ascii')

def doLogin(username, encryptedPass, rsaData):
    global user_agent
    url = 'https://steamcommunity.com/login/dologin/'
    values = {
        'username' : username,
        'password': encryptedPass,
        'emailauth': '',
        'loginfriendlyname': '',
        'captchagid': '-1',
        'captcha_text': '',
        'emailsteamid': '',
        'rsatimestamp': rsaData['timestamp'],
        'remember_login': False,
        'donotcache': str(int(time.time()*1000)),
        'twofactorcode': ''
    }
    headers = {'User-Agent' : user_agent}
    data = None
    while data == None or data['requires_twofactor']:
        if data != None and data['requires_twofactor']:
            values['twofactorcode'] = input('Enter 2FA code: ')
        post = urlencode(values).encode('utf-8')
        req = Request(url, post, headers)
        response = urlopen(req).read()
        data = json.loads(response)
    if not data['success']:
        raise ValueError('Could not log in: ' + data['message'])
    return data

def getWords():
    wordsUrl = 'http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain'
    txt = urlopen(wordsUrl).read()
    return txt.splitlines()

def googleAndUpload(STEAM_ID, WORDS, cookies, sleepTime):
    global DIR

    url = 'https://steamcommunity.com/actions/FileUploader'

    searchQuery = str(random.choice(WORDS))
    searchQuery = searchQuery[2:len(searchQuery)-1]

    imageResultNum = random.randint(0,5)
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
    googleUrl = 'https://www.google.co.in/search?q=' + searchQuery + '&source=lnms&tbm=isch'
    soup = BeautifulSoup(urlopen(Request(googleUrl,headers=header)), 'html.parser')
    images = soup.find_all('div',{'class':'rg_meta'})
    link = json.loads(images[imageResultNum].text)['ou']
    
    raw_img = requests.get(link,stream=True)
    with open(IMG_DIR, 'wb') as out_file:
        shutil.copyfileobj(raw_img.raw, out_file)

    if os.stat(IMG_DIR).st_size >= STEAM_SIZE_LIMIT:
        print("Downloaded image is too big. Downsizing...")
        while os.stat(IMG_DIR).st_size >= STEAM_SIZE_LIMIT:
            img = Image.open(IMG_DIR)
            originalSize = img.size
            img = img.resize((int(originalSize[0] * 0.75), int(originalSize[1] * 0.75)), Image.ANTIALIAS)
            img = img.convert("RGB")
            img.save(IMG_DIR, optimize=True, quality=95)
    
    image = open(IMG_DIR, 'rb')
    params = {'type': 'player_avatar_image', 'sId': STEAM_ID}
    data = {'sessionid': cookies.get('sessionid'), 'doSub': '1'}
    r = requests.post(url=url,params=params,files={'avatar':image},data=data,cookies=cookies)
    print(str(r) + ' for: ' + searchQuery)

    if '#Error_BadOrMissingSteamID' in r.text:
        raise ValueError('Error_BadOrMissingSteamID')

    time.sleep(sleepTime)

if __name__ == '__main__':
    username = input('Steam username: ')
    rsaData = getRSAKey(username)
    encryptedPass = getAndEncryptPass(rsaData)
    sessionid = generateSessionID()

    sleepTime = 0
    while sleepTime < 25:
        sleepTime = int(input('Enter time interval(s) - must be at least 25: '))
    WORDS = getWords()

    while True:
        try:
            loginResp = doLogin(username, encryptedPass, rsaData)
            STEAM_ID = loginResp['transfer_parameters']['steamid']
            cookies = {
                'steamLoginSecure': STEAM_ID + '%7C%7C' + loginResp['transfer_parameters']['token_secure'],
                'sessionid': sessionid
            }

            while True:
                try:
                    googleAndUpload(STEAM_ID, WORDS, cookies, sleepTime)
                except Exception as e:
                    if 'BadOrMissingSteamID' in str(e):
                        # Pass off to the outer loop to redo login
                        raise ValueError(e)
                    else:
                        print(e)
                        print("Redoing image search...")
        except ValueError as e:
            if 'BadOrMissingSteamID' in str(e):
                print('Token expired. Redoing login...')
                rsaData = getRSAKey(username)
            else:
                print(e)
                input('Press any key to exit...')
                exit()
