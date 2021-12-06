import pymongo as mongo

def mongoConnection():
    client = mongo.MongoClient('localhost')
    db = client['fourPaws']
    return db