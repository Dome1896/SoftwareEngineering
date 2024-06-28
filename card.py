from database import Database
class Card:
    '''
    Klasse, welche das Datenmodell für eine Lernkarte stellt.
    '''
    db = Database()
    def __init__(self, question:str, answer:str, category:str, ownerID:int = 0,cardID:int = 0, container_number:int = 4):
        '''
        Initialisiert eine neue Karte mit den angegebenen Parametern.
        :param question: Frage der Karte
        :param answer: Antwort der Karte
        :param category: Kategorie der Karte
        :param ownerID: ID des Benutzers, der die Karte erstellt hat
        :param cardID: ID der Karte
        :param container_number: Nummer des Karteikartenordners, in welchem die Karte aktuell ist
        '''
        self.question = question
        self.answer = answer
        self.category = category
        self.cardID = cardID
        self.ownerID = ownerID

        self.container_number = container_number

        self.tableName = "Cardholder"
    # container up -> wander einer container in richtung 1
    def set_card_one_container_up(self):
        '''
        Setzt die Karte einen Karteikartenordner niedriger. 
        Sollte passieren, sobald die Karte erfolgreich gelernt wurde.
        '''
        if self.container_number != 1:
            Card.db.updateOneValue(self.tableName,attributeKey="cardID", attributeValue=self.cardID
            ,newAttributeKey="container_number", newAttributeValue=self.container_number-1)
    # container up -> wander einer container in richtung 4
    def set_card_one_container_down(self):
        '''
        Setzt die Karte einen Karteikartenordner höher. 
        Sollte passieren, sobald die Karte nicht erfolgreich gelernt wurde.
        '''
        if self.container_number != 4:
            Card.db.updateOneValue(self.tableName,attributeKey="cardID", attributeValue=self.cardID
            ,newAttributeKey="container_number", newAttributeValue=self.container_number+1)

    def makeRequestBody(self):
        '''
        Erstellt den Request-Body für die API, um die Karte zu erstellen.
        :return: request body
        '''
        return {"question" : self.question, "answer" : self.answer, "category" : self.category, "container_number":self.container_number, "ownerID":self.ownerID}
