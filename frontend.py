from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

class MyFloatLayout(FloatLayout):
    def collapse_toolbar(self):
        toolbar = self.ids.toolbar
        button = self.ids.t_button
        # Animation to hide toolbar and move button to the edge
        toolbar_anim = Animation(pos_hint={'x': -0.2}, duration=0.2)
        button_anim = Animation(pos_hint={'x': 0.0001}, duration=0.2)
 
        toolbar_anim.start(toolbar)
        button_anim.start(button)
 
    def expand_toolbar(self):
        toolbar = self.ids.toolbar
        button = self.ids.t_button
 
        toolbar_anim = Animation(pos_hint={'x': 0}, duration=0.2)
        button_anim = Animation(pos_hint={'x': 0.205}, duration=0.2)
 
        toolbar_anim.start(toolbar)
        button_anim.start(button)
 
    def btn(self):
        self.show_popup()
 
    def show_popup(self):
        show = P()
        popupWindow = Popup(title="Add Flashcard", content=show, size_hint=(None, None), size=(400, 400))

        # Speichern der Eingaben aus dem Textfeld
        def save_data(instance):
            value1 = show.ids.questionName.text
            value2 = show.ids.questionAnswer.text
            value3 = show.ids.questionCategory.text

            # Werte in eine Textdatei speichern
            with open('output.txt', 'a') as f:
                f.write(f'{value1},{value2},{value3}\n')

            popupWindow.dismiss()

        show.ids.addCard.bind(on_release=save_data)
        popupWindow.open()
 
    def showCardsWindow(self):
        self.showCards_popup()

    def showCards_popup(self):
        show = ShowCards()
        popupWindow = Popup(title="Show Cards", content=show, size_hint=(None, None), size=(400, 600))

        # Werte aus der Datei lesen
        with open('output.txt', 'r') as f:
            lines = f.readlines()

        # Erstellen und Hinzufügen von Labels für jede Karte
        for line in lines:
            values = line.strip().split(',')
            if len(values) == 3:
                question, answer, category = values
                card_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
                card_layout.add_widget(Label(text=f'Question: {question}', size_hint_y=None, height=30, font_size=16))
                card_layout.add_widget(Label(text=f'Answer: {answer}', size_hint_y=None, height=30, font_size=16))
                card_layout.add_widget(Label(text=f'Category: {category}', size_hint_y=None, height=30, font_size=16))
                show.ids.cards_box.add_widget(card_layout)

        popupWindow.open()
 
 
class P(FloatLayout):
    pass
 
class ShowCards(FloatLayout):
    pass

class MyApp(App):
    def build(self):
        return MyFloatLayout()

if __name__ == "__main__":
    MyApp().run()