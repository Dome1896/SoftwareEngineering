import requests # Importiert die requests-Bibliothek, die HTTP-Anfragen ermöglicht
from configparser import ConfigParser # Importiert ConfigParser, um Konfigurationsdateien zu lesen
import os



class Database:
    '''
    Klasse, die Methoden bereitstellt, um die Verwendung einer Supabase Datenbank zu ermöglichen
    '''
    # Initialisierungsmethode der Klasse, ruft Methoden auf, um URL, Passwort und API-Schlüssel zu erhalten
    def __init__(self):
        '''
        Initialisierungsmethode der Klasse, ruft Methoden auf, um URL, apikey und passwort zu setzen            
        '''
        self.__getUrl()
        self.__getPassword()
        self.__getApiKey()
        # Erstellt ein Header-Dictionary für HTTP-Anfragen mit dem API-Schlüssel und der Autorisierung
        self.__headers = {
            'apikey' : self.__apikey,
            'Authorization' : 'Bearer ' + self.__apikey
        }

    # Methode, um alle Daten aus einer Tabelle zu holen
    def getAllDataFromOneTable(self, tableName:str):
        '''
        :param tableName: Name der Tabelle, aus der die Daten geholt werden sollen
        :return: Eine Liste mit allen Daten aus der Tabelle
        '''
        url = f"{self.__url}{tableName}?select=*"
        # Führt eine GET-Anfrage aus und gibt die Antwort zurück
        response = requests.get(url=url, headers=self.__headers)
        return response

    # Methode, um gefilterte Daten aus einer Tabelle zu holen
    def getDataFromTableWithFilter(self, tableName:str, attributeKey:str, attributeValue:str):
        '''
        :param tableName: Name der Tabelle, aus der die Daten geholt werden sollen
        :param attributeKey: Name des Attributs, nach dem gefiltert werden soll
        :param attributeValue: Wert des Attributs, nach dem gefiltert werden soll
        :return: Eine Liste mit allen Daten aus der Tabelle, die die angegebenen Kriterien erfüllen
        '''
        url = f"{self.__url}{tableName}?{attributeKey}=eq.{attributeValue}&select=*"
        # Führt eine GET-Anfrage aus und gibt die Antwort als JSON zurück
        response = requests.get(url=url, headers=self.__headers)
        return response.json()

    # Methode, um einen Wert in der Tabelle zu aktualisieren
    def updateOneValue(self, tableName:str, attributeKey:str, attributeValue:str, newAttributeKey:str, newAttributeValue:str):
        '''
        Update des entsprechenden Wertes in der Datenbank
        :param tableName: Name der Tabelle, in der der Wert aktualisiert werden soll
        :param attributeKey: Name des Attributs, dessen Wert aktualisiert werden soll
        :param attributeValue: Wert des Attributs, dessen Wert aktualisiert werden soll
        :param newAttributeKey: Name des Attributs, dessen Wert gesetzt werden soll
        :param newAttributeValue: Wert des Attributs, dessen Wert gesetzt werden soll
        
        '''
        url = url = f"{self.__url}{tableName}?{attributeKey}=eq.{attributeValue}"
        # Führt eine PATCH-Anfrage aus, um den Wert zu aktualisieren
        requests.patch(url=url, headers=self.__headers, json={newAttributeKey : newAttributeValue})

    # Methode, um Daten in die Datenbank zu schreiben
    def setDataToDB(self, object:object):
        '''
        :param object: Ein Objekt, das in die Datenbank geschrieben werden soll
        Wichtig: Das Objekt muss die funktion makeRequestBody(): string implementiert haben
        '''
        url = f"{self.__url}{object.tableName}"
        headers = self.__headers
        headers["Prefer"] = "return=minimal"
        # Führt eine POST-Anfrage aus, um die Daten zu senden
        requests.post(url=url, headers=headers, json=object.makeRequestBody())

    # Methode, um alle einzigartigen Werte aus einer Spalte zu erhalten
    def getAllUniqueValuesFromColumn(self, tableName:str, columnName:str):
        '''
        :param tableName: Name der Tabelle, aus der die Daten geholt werden sollen
        :param columnName: Name der Spalte, aus der die Daten geholt werden sollen
        :return: Eine Liste mit allen einzigartigen Werten aus der Spalte
        '''
        url = f"{self.__url}{tableName}?select={columnName}"
        response = requests.get(url=url, headers=self.__headers)
        return response.json()

    # Methode, um den API-Schlüssel aus der Konfigurationsdatei zu lesen
    def __getApiKey(self):
        '''
        setzt das __apikey Attribut auf den Wert des API-Keys aus der Config
        '''
        try:
            cfp = self.__get_config_path()
            self.__apikey = cfp.get("Database", "apikey")
        except:
            print("config.ini is missing or wrong")

    # Methode, um die URL aus der konfigurationsdatei zu lesen
    def __getUrl(self):
        '''
        setzt das __url Attribut auf den Wert der URL aus der Config
        '''
        try:
            cfp = self.__get_config_path()
            self.__url = cfp.get("Database", "url")
        except:
            print("config.ini is missing or wrong")

    # Methode, um das Passwort aus der konfigurationsdatei zu lesen
    def __getPassword(self):
        '''
        setzt das __password Attribut auf den Wert des Passworts aus der Config
        '''
        try:
            cfp = self.__get_config_path()
            self.__password = cfp.get("Database", "password")
        except:
            print("config.ini is missing or wrong")

    
    def __get_config_path(self):
        '''
        Ändert den Pfad zur config.ini, je nach Arbeitsverzeichnis
        :return: Pfad zur Config
        '''
        cfp = ConfigParser()
        if "docs" in os.getcwd():
            cfp.read("../config.ini")
        else:
            cfp.read("config.ini")
        return cfp