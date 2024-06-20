# Importiere die notwendigen Module aus Kivy, um eine einfache GUI-Anwendung zu erstellen.
import kivy
from kivy.app import App
from kivy.uix.label import Label

# Importiere eigene Module, die zur Verwaltung von Datenbanken und Karten verwendet werden.
from database import Database
from card import Card
from controller import Controller
from frontend import FirstApp
from userlogin import *


LoginApp().run()

