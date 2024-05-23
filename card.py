class Card:
    def __init__ (self, title, question, answer, category, cardID = 0):
        self.title = title
        self.question = question
        self.answer = answer
        self.category = category
        self.cardID = cardID

        self.tableName = "Cardholder"

    def makeRequestBody(self):
        return "{"title" : f"{self.title}", "question" : f"{self.question}", "answer" : f"{self.answer}", }"