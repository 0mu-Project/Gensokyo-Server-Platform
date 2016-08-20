import datetime
import setting
from  udockeri import info
from pymongo import MongoClient
from github import Github
client = MongoClient(setting.mongohost)
db = client['Yakumo']
dbc = client['Hakurei']
ins = client['YakumoIns']
class UserContianerReg:
    def add(name):
        cname = dbc[str(name)]
        clist = info(name)
        raw = {"CPUUsage" : clist[0],
                "RAMUsage" : clist[1],
                "RAMLimit" : clist[2],
                "RAMPercent" : clist[3],
                "RX" : clist[4],
                "TX" : clist[5],
                 "date": datetime.datetime.utcnow()
                }
        clist.insert_one(raw)

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

    def addIns(username, password):
        user = ins['Users']
        user.create_index("user", unique=True)
        raw = {"user": username,
                "password": password,
                "date": datetime.datetime.utcnow()}
        print(user.insert_one(raw).inserted_id)

    def login(username):
        try:
            user = db['Users']
            usern = user.find_one({"user": username})
            password = usern['password'] 
        except:
            password = False
        return password

class ReNew:
    def hqs():
        orgname = 'HQSPack'
        gh = Github('m85091081','***REMOVED***')
        org = gh.get_organization(orgname)
        dbhqs = db['HQSPack']
        dbhqs.create_index("name", unique=True)
        for repo in org.get_repos():
            try:
                hqsraw = {'name':repo.full_name, 'date':repo.pushed_at, 'url':repo.clone_url}
                dbhqs.insert_one(hqsraw)
            except:
                key = dbhqs.find_one({"name":repo.full_name})
                print(repo.pushed_at)
                key['date']=repo.pushed_at
                key['url']=repo.clone_url
                dbhqs.save(key)
