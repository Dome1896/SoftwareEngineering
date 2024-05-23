class Card:
    def __init__ (self, title, question, answer, category, cardID = 0):
        self.title = title
        self.question = question
        self.answer = answer
        self.category = category
        self.cardID = cardID

        self.tableName = "Cardholder"
