from kivy.app import App
from kivy.uix.label import Label

from card import Card
from database import Database
from learnmode import Learnmode


class MyApp(App):
    def build(self):
        # Erstelle ein Label-Widget
        return Label(text="Hello, Kivy!")
db = Database()
card = Card(category="Softwareentwicklung", question="Was ist ein Konstruktor?" ,answer="Eine Methode, für das Erzeugen einer Instanz")
db.setDataToDB(card)

learnmode = Learnmode(category="Softwareentwicklung", database=db)
print(learnmode.cards)



# Starte die Anwendung
if __name__ == '__main__':

    MyApp().run()
    
