import requests # Importiert die requests-Bibliothek, die HTTP-Anfragen ermöglicht
from configparser import ConfigParser # Importiert ConfigParser, um Konfigurationsdateien zu lesen
class Database:

    # Initialisierungsmethode der Klasse, ruft Methoden auf, um URL, Passwort und API-Schlüssel zu erhalten
    def __init__(self):
        self.__getUrl()
        self.__getPassword()
        self.__getApiKey()
        # Erstellt ein Header-Dictionary für HTTP-Anfragen mit dem API-Schlüssel und der Autorisierung
        self.__headers = {
            'apikey' : self.__apikey,
            'Authorization' : 'Bearer ' + self.__apikey
        }

    # Methode, um alle Daten aus einer Tabelle zu holen
    def getAllDataFromOneTable(self, tableName):
        url = f"{self.__url}{tableName}?select=*"
        # Führt eine GET-Anfrage aus und gibt die Antwort zurück
        response = requests.get(url=url, headers=self.__headers)
        return response

    # Methode, um gefilterte Daten aus einer Tabelle zu holen
    def getDataFromTableWithFilter(self, tableName, attributeKey, attributeValue):
        url = f"{self.__url}{tableName}?{attributeKey}=eq.{attributeValue}&select=*"
        # Führt eine GET-Anfrage aus und gibt die Antwort als JSON zurück
        response = requests.get(url=url, headers=self.__headers)
        return response.json()

    # Methode, um einen Wert in der Tabelle zu aktualisieren
    def updateOneValue(self, tableName, attributeKey, attributeValue, newAttributeKey, newAttributeValue):
        url = url = f"{self.__url}{tableName}?{attributeKey}=eq.{attributeValue}"
        # Führt eine PATCH-Anfrage aus, um den Wert zu aktualisieren
        requests.patch(url=url, headers=self.__headers, json={newAttributeKey : newAttributeValue})

    # Methode, um Daten in die Datenbank zu schreiben
    def setDataToDB(self, object):
        url = f"{self.__url}{object.tableName}"
        headers = self.__headers
        headers["Prefer"] = "return=minimal"
        # Führt eine POST-Anfrage aus, um die Daten zu senden
        requests.post(url=url, headers=headers, json=object.makeRequestBody())

    # Methode, um alle einzigartigen Werte aus einer Spalte zu erhalten
    def getAllUniqueValuesFromColumn(self, tableName, columnName):
        url = f"{self.__url}{tableName}?select={columnName}"
        response = requests.get(url=url, headers=self.__headers)
        return response.json()

    # Methode, um den API-Schlüssel aus der Konfigurationsdatei zu lesen
    def __getApiKey(self):
        cfp = ConfigParser()
        try:
            cfp.read("./config.ini")
            self.__apikey = cfp.get("Database", "apikey")
        except:
            print("config.ini is missing or wrong")

    # Methode, um die URL aus der konfigurationsdatei zu lesen
    def __getUrl(self):
        cfp = ConfigParser()
        try:
            cfp.read("config.ini")
            self.__url = cfp.get("Database", "url")
        except:
            print("config.ini is missing or wrong")

    # Methode, um das Passwort aus der konfigurationsdatei zu lesen
    def __getPassword(self):
        cfp = ConfigParser()
        try:
            cfp.read("config.ini")
            self.__password = cfp.get("Database", "password")
        except:
            print("config.ini is missing or wrong")