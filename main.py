import kivy
from kivy.app import App
from kivy.uix.label import Label
from database import Database
from card import Card

class MyApp(App):
    def build(self):
        # Erstelle ein Label-Widget
        return Label(text="Hello, Kivy!")
db = Database()
card = Card("tst", "tsest", "testcate")
db.setDataToDB(card)
db.getAllDataFromOneTable("Cardholder")

# Starte die Anwendung
if __name__ == '__main__':

    MyApp().run()
    
