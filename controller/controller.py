# Importiert die notwendigen Module und Klassen aus Kivy.
from kivy.app import App
from kivy.lang import Builder
# Importiert die benutzerdefinierten Module Database und Card.
from models.database.database import Database
from models.card.card import Card
from models.apiHandler.apihandler import APIHandler
from models.user.user import User


# Definiert die Klasse Controller, die von Kivy's App-Klasse erbt.
class Controller():
    '''
    Klasse, welche die Schnittstelle zwischen backend und frontend stellt.
    Alle Methoden sind Klassenmethoden, um einen einfachen Zugriff zu ermöglichen
    '''

    # Erstellt eine Klassenvariable 'db', die eine Instanz der Database-Klasse ist.
    db = Database()
    kiApi = APIHandler()

    # Definiert eine Klassenmethode zum Erstellen einer neuen Karte.
    @classmethod
    def createCard(cls, question: str, answer: str, category: str):
        '''
        Erstellt eine neue Karte mit den übergebenen Parametern.
        :param question: Frage der Karte
        :param answer: Antwort der Karte
        :param category: Kategorie der Karte
        :return: None
        '''
        # Erstellt eine neue Karte mit den angegebenen Attributen.
        card = Card(question, answer, category, ownerID=cls.userID)
        # Speichert die Karte in der Datenbank.
        cls.db.setDataToDB(card)

    @classmethod
    def create_user(cls, username:str, password:str, userID:str):
        '''
        Erstellt einen neuen User mit den übergebenen Parametern.
        :param username: Username des Users
        :param password: Passwort des Users
        :param userID: ID des Users
        :return: None
        '''
        cls.user = User(username, password, userID)
        cls.userID = userID
    # Definiert eine Klassenmethode, die alle Karten für eine bestimmte Kategorie zurückgibt.
    @classmethod
    def getAllCardsForCategory(cls, category: str):
        '''
        Gibt alle Karten für eine bestimmte Kategorie zurück.
        :param category: Kategorie der Karten - wenn category = "*", gibt alle Karten für den User zurück
        :return: Liste von Karten
        '''
        # Initialisiert eine leere Liste, um die Karten zu speichern.
        cardList = []
        if category != "*":

            # Ruft alle Karten der angegebenen Kategorie aus der Datenbank ab.
            for card in cls.db.getDataFromTableWithFilter("Cardholder", "category", category):
                # Fügt jede Karte der Liste hinzu, indem eine Card-Instanz erstellt wird.
                if card["ownerID"] == cls.userID:
                    cardList.append(Card(cardID=card["cardID"], question=card["question"], answer=card["answer"], category=card["category"], container_number=card["container_number"]))
        # gibt alle Karten des Users zurück
        else:
            for card in cls.db.getDataFromTableWithFilter("Cardholder", "ownerID", cls.userID):
                cardList.append(Card(cardID=card["cardID"], question=card["question"], answer=card["answer"], category=card["category"], container_number=card["container_number"]))
        # Gibt die Liste der Karten zurück.
        return cardList

    # Definiert eine Klassenmethode, die eine Karte aus einer Kartenliste extrahiert.
    @classmethod
    def extractOneCardFromCardList(cls, cardList:dict[Card]):
        '''
        Extrahiert eine Karte aus einer Kartenliste.
        :param cardList: Liste von Karten
        :return: Karte
        '''
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
        '''
        Gibt alle eindeutigen Kategorien zurück.
        :return: Liste von Kategorien
        '''
        # Ruft alle eindeutigen Kategorien aus der Datenbank ab.
        categories = cls.db.getAllUniqueValuesFromColumn("Cardholder", "category,ownerID")
        # Initialisiert eine leere Liste, um die Kategorien zu speichern.
        categoriesList = []
        # Iteriert durch die Kategorien und fügt sie der Liste hinzu, wenn sie nicht bereits vorhanden sind.
        for category in categories:
            i = category["category"]
            user = category["ownerID"]
            if i not in categoriesList:
                if user == cls.userID:
                    categoriesList.append(i)
        # Gibt die Liste der Kategorien zurück.
        return categoriesList
    @classmethod
    def set_card_on_container_up(cls, card : Card):
        '''
        Setzt den container_number Wert der Karte einen höher -> wenn die 
        :param card: Karte
        :return: None
        '''
        card.set_card_one_container_up()

    @classmethod
    def set_card_on_container_down(cls, card : Card):
        card.set_card_one_container_down()

    @classmethod
    def add_cards_to_filtered_cards(cls, filter_number:str, all_cards_list:dict[Card]):
        print(len(all_cards_list))
        filtered_cards = []
        for card in all_cards_list:
            if card.container_number == filter_number:
                filtered_cards.append(card)
        return filtered_cards

    @classmethod
    def del_cards_in_filtered_cards(cls, filter_number:str, filtered_list:dict[Card]):
        cards_to_delete = []
        for card in filtered_list:
            if card.container_number == filter_number:
                cards_to_delete.append(card.cardID)
        return cards_to_delete
    
    @classmethod
    def generate_answer(cls, question:str, category:str=""):
        return cls.kiApi.generate_answer(question, category)
    
    @classmethod
    def verify_credentials(cls, username:str, password:str):
        user = cls.db.getDataFromTableWithFilter(tableName="User",attributeKey="username", attributeValue=username)
        if user and user[0]["password"] == password:
            cls.userID = user[0]["userID"]
            return True, cls.userID
        else:
            return False, 0
    @classmethod
    def register_user(cls, username:str, password:str):
        cls.db.setDataToDB(User(username, password))


        



