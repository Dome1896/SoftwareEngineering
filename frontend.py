from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from controller import Controller

class MyFloatLayout(FloatLayout):


    def get_categories(self):
        return Controller.getAllCategories()

        

    toolbar_expanded = True  # Zustand der Toolbar
    def toggle_toolbar(self):
        button = self.ids.t_button
        toolbar = self.ids.toolbar

        if self.toolbar_expanded:
            # Animation to hide toolbar
            toolbar_anim = Animation(pos_hint={'x': -0.2}, duration=0.2)
            button_anim = Animation(pos_hint={'x': 0.01}, duration=0.2)
        else:
            # Animation to show toolbar
            toolbar_anim = Animation(pos_hint={'x': 0}, duration=0.2)
            button_anim = Animation(pos_hint={'x': 0.2}, duration=0.2)

        toolbar_anim.start(toolbar)
        button_anim.start(button)
        self.toolbar_expanded = not self.toolbar_expanded

    def btn(self):
        self.show_popup()

    def show_popup(self):
        show = P()
        popupWindow = Popup(title="Add Flashcard", content=show, size_hint=(None, None), size=(400, 400))

        def save_data(instance):
            value1 = show.ids.questionName.text
            value2 = show.ids.questionAnswer.text
            value3 = show.ids.questionCategory.text
            Controller.createCard(question=value1, answer=value2, category=value3)
            popupWindow.dismiss()

        show.ids.addCard.bind(on_release=save_data)
        popupWindow.open()


class P(FloatLayout):
    pass

class FirstWindow(Screen, MyFloatLayout):
    def getCardsForCategory(self):
        SecondWindow.cardList = Controller.getAllCardsForCategory("Softwareentwicklung")

class SecondWindow(Screen):
    
    cardIndex = 0
    def nextCard(self):
        if self.cardIndex < len(self.cardList):
            card = self.cardList[self.cardIndex]
            self.cardIndex += 1
            self.ids.learnmodeQuestion.text = card.question
            self.ids.learnmodeAnswer.text = card.answer
            self.ids.learnmodeCategory.text = card.category
        else:
            self.ids.learnmodeQuestion.text = "Das wars!"
            self.ids.learnmodeAnswer.text = "Du hast alle Karten der Kategorie gelernt!"
            self.ids.learnmodeCategory.text = "Herzlichen Glückwunsch!"
    def resetLearnmode(self):

        self.ids.learnmodeQuestion.text = "Frage"
        self.ids.learnmodeAnswer.text = "Antwort"
        self.ids.learnmodeCategory.text = "Kategorie"
        self.cardIndex = 0

class WindowManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        Builder.load_file('my.kv')
        return MyFloatLayout()

kv = Builder.load_file('first_window.kv')

class FirstApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    FirstApp().run()