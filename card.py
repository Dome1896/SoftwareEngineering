from database import Database
class Card:
    db = Database()
    def __init__(self, question, answer, category, cardID = 0, container_number:int = 4):
        self.question = question
        self.answer = answer
        self.category = category
        self.cardID = cardID

        self.container_number = container_number

        self.tableName = "Cardholder"
    # container up -> wander einer container in richtung 1
    def set_card_one_container_up(self):
        if self.container_number != 1:
            Card.db.updateOneValue(self.tableName,attributeKey="cardID", attributeValue=self.cardID
            ,newAttributeKey="container_number", newAttributeValue=self.container_number-1)
    # container up -> wander einer container in richtung 4
    def set_card_one_container_down(self):
        if self.container_number != 4:
            Card.db.updateOneValue(self.tableName,attributeKey="cardID", attributeValue=self.cardID
            ,newAttributeKey="container_number", newAttributeValue=self.container_number+1)

    def makeRequestBody(self):
        return {"question" : self.question, "answer" : self.answer, "category" : self.category, "container_number":self.container_number}
