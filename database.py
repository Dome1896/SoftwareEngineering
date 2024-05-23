import requests
from configparser import ConfigParser
from supabase import *
class Database:
    
    def __init__(self):
        self.__getUrl()
        self.__getPassword()
        self.__getApiKey()
        self.__headers = {
            'apikey' : self.__apikey,
            'Authorization' : 'Bearer ' + self.__apikey
        }
    def getAllDataFromOneTable(self, tableName):
        url = f"{self.__url}{tableName}?select=*"
        self.__headers
        response = requests.get(url=url, headers=self.__headers)
        return response
    
    def getDataFromTableWithFilter(self, tableName, attributeKey, attributeValue):
        url = f"{self.__url}{tableName}?{attributeKey}=eq.{attributeValue}&select=*"
        response = requests.get(url=url, headers=self.__headers)
        return response.json()
    
    def updateOneValue(self, tableName, attributeKey, attributeValue, newAttributeKey, newAttributeValue):
        url = url = f"{self.__url}{tableName}?{attributeKey}=eq.{attributeValue}"
        requests.patch(url=url, headers=self.__headers, json={newAttributeKey : newAttributeValue})

    def setDataToDB(self, object):
        url = f"{self.__url}{object.tableName}"
        headers = self.__headers
        headers["Prefer"] = "return=minimal"
        requests.post(url=url, headers=headers, json=object.makeRequestBody())
    

    def __getApiKey(self):
        cfp = ConfigParser()
        try:
            cfp.read("./config.ini")
            self.__apikey = cfp.get("Database", "apikey")
        except:
            print("config.ini is missing or wrong")

    def __getUrl(self):
        cfp = ConfigParser()
        try:
            cfp.read("config.ini")
            self.__url = cfp.get("Database", "url")
        except:
            print("config.ini is missing or wrong")

    def __getPassword(self):
        cfp = ConfigParser()
        try:
            cfp.read("config.ini")
            self.__password = cfp.get("Database", "password")
        except:
            print("config.ini is missing or wrong")

#db = Database()
#print(db.getDataFromTableWithFilter("users", "id" , "1"))