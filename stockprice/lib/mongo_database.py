from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/stocks")
db = client['stocks']

def listTickers():
    for sym in db.collection_names():
        print(sym)
        yield(sym)

if __name__ == '__main__':
    pass
