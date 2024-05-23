class Card:
    def __init__ (self, question, answer, category, cardID = 0):
        self.question = question
        self.answer = answer
        self.category = category
        self.cardID = cardID

        self.tableName = "Cardholder"

    def makeRequestBody(self):
        return {"question" : self.question, "answer" : self.answer, "category" : self.category}