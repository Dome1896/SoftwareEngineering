from kivy.app import App
from kivy.lang import Builder
from database import Database
from card import Card

Builder.load_file('my.kv')
class Controller(App):

    db = Database()

    # erstellen
    @classmethod
    def createCard(cls, question: str, answer: str, category: str):
        card = Card(question, answer, category)
        cls.db.setDataToDB(card)

    @classmethod
    def getAllCardsForCategory(cls, category: str):
        cardList = []

        for card in cls.db.getDataFromTableWithFilter("Cardholder", "category", category):
            cardList.append(Card(cardID=card["cardID"], question=card["question"], answer=card["answer"], category=card["category"]))
        return cardList

    @classmethod
    def extractOneCardFromCardList(cls, cardList):
        if len(cardList) > 0:
            card = cardList.pop()
            return card
        return None

    @classmethod
    def getAllCategories(cls):
        '''
        Returns
            an Array with all unique categories in the table "Cardholder"
        '''
        categories = cls.db.getAllValuesFromColumn("Cardholder", "category")
        categoriesList = []
        for category in categories:
            i = category["category"]
            if i not in categoriesList:
                categoriesList.append(i)
        return categoriesList



