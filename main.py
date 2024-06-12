import kivy
from kivy.app import App
from kivy.uix.label import Label
from database import Database
from card import Card
from controller import Controller

db = Database()
card = Card("tst", "tsest", "testcate")
db.setDataToDB(card)
# Alle Daten aus der Tabelle abrufen
all_users = db.getAllDataFromOneTable("Cardholder")
print(all_users)

# Daten aus der Tabelle mit Filter abrufen
filtered_card = db.getDataFromTableWithFilter("Cardholder", "cardID", "17")
print(filtered_card)

cards = db.getDataFromTableWithFilter(tableName="Cardholder", attributeKey="category", attributeValue="Softwareentwicklung")
print(cards)
print(db.getAllValuesFromColumn("Cardholder", "category"))
print(Controller.getAllCategories())