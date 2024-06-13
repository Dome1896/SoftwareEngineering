# Importiere die notwendigen Module aus Kivy, um eine einfache GUI-Anwendung zu erstellen.
import kivy
from kivy.app import App
from kivy.uix.label import Label

# Importiere eigene Module, die zur Verwaltung von Datenbanken und Karten verwendet werden.
from database import Database
from card import Card
from controller import Controller

# Erstelle eine Instanz der Datenbankklasse.
db = Database()

# Erstelle eine Karte mit Beispielwerten und füge sie zur Datenbank hinzu.
card = Card("tst", "tsest", "testcate")
db.setDataToDB(card)

# Rufe alle Daten aus der Tabelle "Cardholder" ab und drucke sie aus.
all_users = db.getAllDataFromOneTable("Cardholder")
print(all_users)

# Daten aus der Tabelle mit Filter abrufen
filtered_card = db.getDataFromTableWithFilter("Cardholder", "cardID", "17")
print(filtered_card)

cards = db.getDataFromTableWithFilter(tableName="Cardholder", attributeKey="category", attributeValue="Softwareentwicklung")
print(cards)
print(db.getAllUniqueValuesFromColumn("Cardholder", "category"))
print(Controller.getAllCategories())