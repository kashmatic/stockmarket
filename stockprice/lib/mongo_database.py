from pymongo import MongoClient

import os

#client = MongoClient("mongodb://localhost:27017/stocks")
client = MongoClient(os.environ.get('DATABASE_URI'))
print(client)

db = client['stocks']

def listTickers():
    for sym in db.collection_names():
        print(sym)
        yield(sym)

if __name__ == '__main__':
    pass
