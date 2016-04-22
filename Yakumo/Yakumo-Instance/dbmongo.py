import datetime
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['Yakumo']
class InitDB:
    user = db['Users']

class User:
    def add(username, password, admin):
        user = db['Users']
        user.create_index("user", unique=True)
        raw = {"user": username,
                "password": password,
                "admin": admin,
                "date": datetime.datetime.utcnow()}
        print(user.insert_one(raw).inserted_id)

    def login(username):
        user = db['Users']
        usern = user.find_one({"user": username})
        return usern['password'] 


