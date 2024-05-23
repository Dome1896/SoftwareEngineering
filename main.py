import kivy
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        # Erstelle ein Label-Widget
        return Label(text="Hello, Kivy!")

# Starte die Anwendung
if __name__ == '__main__':
    MyApp().run()
