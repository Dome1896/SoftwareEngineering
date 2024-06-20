from configparser import ConfigParser
from openai import OpenAI
class APIHandler:
    def __init__(self):
        self.client = OpenAI(api_key=self.__getApiKey())
    
    def genere_answer(self, question, category=""):
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
        cfp = ConfigParser()
        try:
            cfp.read("config.ini")
            __apikey = cfp.get("API", "apikey")
            return __apikey
        except:
            print("config.ini is missing or wrong")
            
    
        
