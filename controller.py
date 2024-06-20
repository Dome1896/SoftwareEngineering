# Importiert die notwendigen Module und Klassen aus Kivy.
from kivy.app import App
from kivy.lang import Builder
# Importiert die benutzerdefinierten Module Database und Card.
from database import Database
from card import Card
from apihandler import APIHandler

# Lädt die Kivy-Datei 'my.kv', die die UI-Definitionen enthält.
Builder.load_file('my.kv')

# Definiert die Klasse Controller, die von Kivy's App-Klasse erbt.
class Controller(App):

    # Erstellt eine Klassenvariable 'db', die eine Instanz der Database-Klasse ist.
    db = Database()
    kiApi = APIHandler()

    # Definiert eine Klassenmethode zum Erstellen einer neuen Karte.
    @classmethod
    def createCard(cls, question: str, answer: str, category: str):
        # Erstellt eine neue Karte mit den angegebenen Attributen.
        card = Card(question, answer, category)
        # Speichert die Karte in der Datenbank.
        cls.db.setDataToDB(card)

    # Definiert eine Klassenmethode, die alle Karten für eine bestimmte Kategorie zurückgibt.
    @classmethod
    def getAllCardsForCategory(cls, category: str):
        # Initialisiert eine leere Liste, um die Karten zu speichern.
        cardList = []

        # Ruft alle Karten der angegebenen Kategorie aus der Datenbank ab.
        for card in cls.db.getDataFromTableWithFilter("Cardholder", "category", category):
            # Fügt jede Karte der Liste hinzu, indem eine Card-Instanz erstellt wird.
            cardList.append(Card(cardID=card["cardID"], question=card["question"], answer=card["answer"], category=card["category"], container_number=card["container_number"]))
        # Gibt die Liste der Karten zurück.
        return cardList

    # Definiert eine Klassenmethode, die eine Karte aus einer Kartenliste extrahiert.
    @classmethod
    def extractOneCardFromCardList(cls, cardList):
        # Überprüft, ob die Liste nicht leer ist.
        if len(cardList) > 0:
            # Entfernt und gibt die letzte Karte aus der Liste zurück.
            card = cardList.pop()
            return card
        # Gibt None zurück, wenn die Liste leer ist.
        return None

    # Definiert eine Klassenmethode, die alle eindeutigen Kategorien zurückgibt.
    @classmethod
    def getAllCategories(cls):
        # Ruft alle eindeutigen Kategorien aus der Datenbank ab.
        categories = cls.db.getAllUniqueValuesFromColumn("Cardholder", "category")
        # Initialisiert eine leere Liste, um die Kategorien zu speichern.
        categoriesList = []
        # Iteriert durch die Kategorien und fügt sie der Liste hinzu, wenn sie nicht bereits vorhanden sind.
        for category in categories:
            i = category["category"]
            if i not in categoriesList:
                categoriesList.append(i)
        # Gibt die Liste der Kategorien zurück.
        return categoriesList
    @classmethod
    def set_card_on_container_up(cls, card : Card):
        card.set_card_one_container_up()

    @classmethod
    def set_card_on_container_down(cls, card : Card):
        card.set_card_one_container_down()

    @classmethod
    def add_cards_to_filtered_cards(cls, filter_number, all_cards_list):
        print(len(all_cards_list))
        filtered_cards = []
        for card in all_cards_list:
            if card.container_number == filter_number:
                filtered_cards.append(card)
        return filtered_cards

    @classmethod
    def del_cards_in_filtered_cards(cls, filter_number, filtered_list):
        cards_to_delete = []
        for card in filtered_list:
            if card.container_number == filter_number:
                cards_to_delete.append(card.cardID)
        return cards_to_delete
    
    @classmethod
    def generate_answer(cls, question, category=""):
        return cls.kiApi.genere_answer(question, category)

        



