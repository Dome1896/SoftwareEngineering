import kivy
from kivy.app import App
from kivy.uix.label import Label
from database import Database
from card import Card

# class MyApp(App):
#     def build(self):
#         # Erstelle ein Label-Widget
#         return Label(text="Hello, Kivy!")
db = Database()
card = Card( "tst", "tsest", "testcate")
db.setDataToDB(card)

# Alle Daten aus der Tabelle abrufen
all_users = db.getAllDataFromOneTable("Cardholder")
print(all_users)

# Daten aus der Tabelle mit Filter abrufen
filtered_card = db.getDataFromTableWithFilter("Cardholder", "id", "17")
print(filtered_card)

hs = 0
# Starte die Anwendung
# if __name__ == '__main__':

#     MyApp().run()
    
