from configparser import ConfigParser
from openai import OpenAI
import os

class APIHandler:
    def __init__(self):
        self.client = OpenAI(api_key=self.__getApiKey())
    
    def generate_answer(self, question:str, category:str=""):
        '''
        Generiert die Antwort auf die Frage. Bezieht die Kategorie mit ein.  
        :param question: Die Frage, auf die eine Antwort generiert werden soll.
        :param category: unrequired Die Kategorie, in der die Frage gestellt wurde.
        :return: Die generierte, perfekte Antwort.
        '''
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "Just answer to the following question in the Language the question is transfered. Keep it short, max is 200 symbols."},
            {"role": "user", "content": f"Frage: {question}. Kategorie: {category}"}
                    ]
            )
        
        perfectAnswer = completion.choices[0].message.content
        return perfectAnswer
    
   
    def __getApiKey(self):
        '''
        Liest die API Key aus der config.ini Datei.
        Setzt das __apikey attribut des Objektes
        '''
        try:
            cfp = self.__get_config_path()
            __apikey = cfp.get("API", "apikey")
            return __apikey
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
            
    
        
