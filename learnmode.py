# wenn der Lernmdous ausgewählt wird, dann wird dieser als Objekt der entsprechenden Kategorie erstellt
from card import Card
from database import Database
class Learnmode():
    
    def __init__(self, category : str, database : Database):
        self.category = category
        self.database = database
        self.cards = self.getCardsByCategory()


    def getCardsByCategory(self):
        '''
        #return
        gibt eine List mit allen Karten der Kategorie des Learnmodes zurück
        '''
        # erstellt eine Liste mit allen Karten der passenden Kategorie in der Datenbank
        cardByCategoryList = self.database.getDataFromTableWithFilter(tableName="Cardholder", attributeKey="category", attributeValue=self.category)
        cards = []
        for card in cardByCategoryList:
            # für jeden Karte in der Datenbank, wird ein Objekt erstellt und diese der Liste hinzugefügt
            cards.append(Card(question= card["question"], answer=card["answer"], category=["category"], cardID=["cardID"]))
        return cards
