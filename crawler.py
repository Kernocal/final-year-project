import time
from pageControl import *
from connectDB import connectToCol
from bs4 import BeautifulSoup
from scraper import addProduct, addVendor, generateCollection, checkDuplicate, getObjectCount, addCategories, generateTime
from random import randrange, shuffle

def continueCrawling(count):
    return input("Continue crawling? {0} categories crawled so far (y/n) ".format(count))

def generateDatabaseSkeleton():
    date = generateTime()
    generateCollection('pages', date[0])
    generateCollection('products', date[0])
    generateCollection('vendors', date[0])
    generateCollection('categories', date[0])

def getNextCategoryID(date, index=0):
    collection = connectToCol(date)
    categories = collection.find_one({'name': 'categories'})
    category = categories['values'][str(index)]
    return category['id']

def checkRobot(pageSoup):
    if 'Hello robot!' in str(pageSoup.find('h2')):
        print("Crawler has been detected as a robot.")
        return False
    return True

def baseCrawl(session, name):
    seconds = float(randrange(500, 700)) / 100
    print("Anti Bot Detection: waiting {0} seconds before crawling next page".format(seconds))
    time.sleep(seconds)
    page = session.get("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/" + name)
    pageSoup = BeautifulSoup(page.text, 'html.parser')
    archivePage(name.replace("?", "？"), page)
    return pageSoup

def crawlPage(session, name):
    pageSoup = baseCrawl(session, name)
    if checkRobot(pageSoup) == False:
        return False
    productsObject = pageSoup.select('div[class~=listinglist]')
    for product in productsObject:
        addProduct(product)

def crawlVendor(session, name, date):
    pageSoup = baseCrawl(session, name)
    if checkRobot(pageSoup) == False:
        return False
    addVendor(name.split('=')[1], date)

def crawlCategory(session, id, date):
    vendorCount = 1
    name = "welcome?sc=" + str(id)
    if checkDuplicate(name.replace("?", "？"), 'name', 'pages', date):
        return True
    category = session.get("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/{0}".format(name))
    archivePage(name.replace("?", "？"), category)
    categorySoup = BeautifulSoup(category.text, 'html.parser')
    pageObject = [data for data in categorySoup.select('div[class~=panel-heading] > strong') if 'Found' in str(data)]
    pageAmount = str(pageObject).split()[3]
    productsObject = categorySoup.select('div[class~=listinglist]')
    for product in productsObject:
        addProduct(product)
    vendorLinks = [str(vendor).split('"')[1] for vendor in categorySoup.select('p > a[href*="userinfo"]') if "userinfo" in str(vendor).split('"')[1]]
    for page in range(1, int(pageAmount)):
        name = "welcome?sc={0}&page={1}".format(str(id), page)
        if checkDuplicate(name.replace("?", "？"), 'name', 'pages', date):
            continue
        if crawlPage(session, name) == False:
            return False
        if vendorCount == 6:
            vendorCount = 0
            if crawlVendor(session, vendorLinks[int(page / 6)], date) == False:
                return False
        vendorCount += 1
    return True

def startCrawler(session, date):
    count = 0
    addCategories()
    categories = list(range(int(getObjectCount("categories", date))))
    shuffle(categories)
    print("There are {0} categories left to crawl.".format(len(categories)))
    for category in categories:
        id = getNextCategoryID(date, category)
        if crawlCategory(session, id, date) == False:
            print("Trying to log out and quit.")
            logoutWhiteHouse(session)
            return None
        count += 1
        if continueCrawling(count) != "y":
            print("Logging out and quitting.")
            logoutWhiteHouse(session)
            break
        seconds = float(randrange(1000, 1500)) / 100
        print("Anti Bot Detection: Waiting {0} seconds before crawling next category.".format(seconds))
        time.sleep(seconds)
    print("Finished crawling {0} categories, {1} products, {2} vendors.".format(count, getObjectCount("products", date), getObjectCount("vendors", date)))

def logoutWhiteHouse(session):
    logout = session.get("http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion/logout")
    logoutSoup = BeautifulSoup(logout.text, 'html.parser')
    logoutSucess = logoutSoup.find_all('h2')
    if 'Before' not in str(logoutSucess):
        print("Failed to logout.")
    else:
        print("Logged out.")