import time
from bs4 import BeautifulSoup
from random import choice
from captchaData import writeImages
from captchaGUI import solveCAPTCHA_manually
from pageControl import archivePage, generateTime
from crawler import startCrawler

#ACCOUNT DETAILS
whiteHouseAccount = {'username': 'zelciu787', 'password': "&*(ytrtytry4"}
#whiteHouseAccount1 = {'username': 'testing1tusop', 'password': "TUSOP^&*678^*&*;'#';#"}
#whiteHouseAccount2 = {'username': 'whathowbeitdo', 'password': "567rtyujk&*"}

def startAuthentication(session):
    print("\nStarting authentication process.")
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'}
    redirect = session.get("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion")
    archivePage("redirect", redirect)

    redirectSoup = BeautifulSoup(redirect.text, 'html.parser')
    secondsDiv = redirectSoup.find_all('div', {'class':'wait'})
    seconds = str(secondsDiv[0]).split('about ')[1].split()[0]

    print("Waiting to redirect, about {0} seconds.".format(seconds))
    time.sleep(int(seconds)+2)
    getCAPTCHA(session)

def getCAPTCHA(session):
    captcha = session.get("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/")
    archivePage("captcha", captcha)
    captchaSoup = BeautifulSoup(captcha.text, 'html.parser')

    labels = captchaSoup.find_all('label')
    wordToFind = str(str(labels[0]).split()[4].split('<')[0])

    unfliteredURLData = captchaSoup.find_all('label', attrs={'for': True})
    captchaURLData = []
    for i in unfliteredURLData:
        if "background" in str(i):
            captchaURLData.append((str(i).split('url(')[1]).split(')')[0])
    writeImages(captchaURLData)
    solveCAPTCHA_manually(session, captchaURLData, wordToFind)

def whiteHouseLogin(session, answers):
    captchaPayload = {'cap': sorted(answers)}
    session.headers['Referer'] = session.headers['Origin'] = 'http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/'
    submitCaptcha = session.post("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/", data=captchaPayload)
    archivePage("initcap", submitCaptcha)

    initcapSoup = BeautifulSoup(submitCaptcha.text, 'html.parser')
    captchaSucess = initcapSoup.find_all('h2')
    if 'Before' not in str(captchaSucess):
        print("Failed captcha, try again.")
        return getCAPTCHA(session)
    print("Correct CAPTCHA answers.")
    initcap = session.post("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/initcap")
    archivePage("login", initcap)

    timeout = [10, 20, 30, 60, 720, 1440, 2280]
    loginPayload = whiteHouseAccount
    loginPayload['timeout'] = choice(timeout)

    login = session.post("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/login", data=loginPayload)
    archivePage("homeNews", login)
    print("Logged in using account '{0}' with a timeout of '{1}' minutes of inactivity.".format(loginPayload['username'], loginPayload['timeout']))

    newsPayload = {'dismiss_news': 'dismiss_news'}
    session.headers['Referer'] = 'http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/welcome'

    exitNews = session.post("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/welcome", data=newsPayload)
    archivePage("welcome", exitNews)

    startCrawler(session, str(generateTime()[0]))