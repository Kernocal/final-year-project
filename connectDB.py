import pymongo

def connectToMongoDB():
    try:
        return pymongo.MongoClient("mongodb://localhost:27017/")
    except (AttributeError, pymongo.errors.OperationFailure):
        print("Connection to MongoDB failed.")

def connectToCol(collectionName):
    connection = connectToMongoDB()
    database = connection["whitehouse"]
    collection = database[collectionName]
    return collection