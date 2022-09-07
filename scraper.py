import re
import datetime
from bs4 import BeautifulSoup
from connectDB import connectToCol

def generateTime():
    return str(datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")).split()

def createPageSoup(name, date):
    name = name.replace('?', '？')
    with open('archive/{0}/{1}.html'.format(date, name), 'r') as f:
        pageData = f.read()
    soup = BeautifulSoup(pageData, 'html.parser')
    return soup

def addObject(name, data, date):
    collection = connectToCol(date)
    objectDict = collection.find_one({'name': str(name)})
    currentValue = str(len(objectDict['values']))
    objectDict['values'][currentValue] = data
    collection.update_one({'name': str(name)}, {"$set": objectDict})

def getObjectCount(name, date):
    collection = connectToCol(date)
    objectDict = collection.find_one({'name': str(name)})
    return len(objectDict['values'])

def generateCollection(name, date):
    collection = connectToCol(date)
    objectDict = {'name': str(name)}
    if collection.find_one(objectDict) != None:
        return None
    objectDict['values'] = {}
    collection.insert_one(objectDict)
    print("Generated {0} collection.".format(name))

def getCategoryData(categoryData):
    category = {}
    category['id'] = categoryData.split('welcome?sc=')[1].split('">')[0]
    category['name'] = categoryData.split('">')[1].split(' <span')[0]
    category['amountOfListings'] = categoryData.split('badge">')[1].split('</span')[0]
    return category

def getProductData(productData):
    product = {}
    productSoup = BeautifulSoup(str(productData), 'html.parser')
    product['id'] = str(productSoup.select('a[href*="sendmessage"]')[0]['href']).split('=')[2]
    product['title'] = productSoup.select('p > a[href*="welcome"]')[1].text
    product['category'] = productSoup.select('p > a[href*="welcome"]')[0].text
    product['price'] = productSoup.select('div[class~=col-md-4] > p > strong')[0].text
    product['shipsFrom'] = str(productSoup.select('li[class~=text-left] > p')[1]).split(': ')[1].split('<')[0]
    product['shipsTo'] = str(productSoup.select('li[class~=text-left] > p')[2]).split(': ')[1].split('<')[0]
    product['vendor'] = str(productSoup.select('a[href*="sendmessage"]')[0]['href']).split('=')[1].split('&')[0]
    return product

def splitVendorData(data):
    return str(data).split('>')[1].split('<')[0]

def getVendorData(vendorName, date):
    vendor = {}
    vendorSoup = createPageSoup('userinfo?user=' + str(vendorName), date)
    vendorData = vendorSoup.select('tr > td')
    vendor['username'] = splitVendorData(vendorData[1])
    vendor['joined'] = splitVendorData(vendorData[3])
    vendor['feedback'] = str(vendorData[11]).split('/ ')[1].split(' r')[0]
    vendor['sales'] = str(vendorData[13]).split('[ ')[1].split(' s')[0]
    vendor['publicKey'] = vendorSoup.select('td > textarea')[0].text.replace('\n', '')
    vendor['fingerprint'] = vendorSoup.select('td[class~=wwrap]')[0].text
    return vendor

def checkDuplicate(id, name, dataset, date):
    collection = connectToCol(date)
    objectDict = collection.find_one({'name': str(dataset)})
    for item in objectDict['values']:
        if objectDict['values'][str(item)][name] == str(id):
            return True
    return False

def addPage(page, date, time):
    pageData = {'name': page, 'time': time}
    if checkDuplicate(page, 'name', 'pages', date):
        return None
    addObject('pages', pageData, date)

def addCategories():
    time = generateTime()
    collection = connectToCol(time[0])
    if str(collection.find_one({'name': 'categories'})['values']) != '{}':
        return False
    soup = createPageSoup("welcome", time[0])
    categoriesData = soup.find_all("a", href=re.compile("sc"))
    for category in categoriesData:
        addObject('categories', getCategoryData(str(category)), time[0])
        if str(category).split('welcome?sc=')[1].split('">')[0] == '49':
            break
    print("Archived category data at {0}".format(time[1]))

def addProduct(product):
    time = generateTime()
    if checkDuplicate(getProductData(product)['id'], 'id', 'products', time[0]):
        return None
    addObject('products', getProductData(product), time[0])
    print("Archived product {0} at {1}".format(getProductData(product)['id'], time[1]))

def addVendor(vendor, date):
    if checkDuplicate(vendor, 'username', 'vendors', date):
        return None
    addObject('vendors', getVendorData(vendor, date), date)

def getTotalListings(date):
    col = connectToCol(date)
    listings = 0
    objectDict = col.find_one({'name': 'categories'})
    for listing in objectDict['values']:
        listings += int(objectDict['values'][str(listing)]['amountOfListings'])
    return listings