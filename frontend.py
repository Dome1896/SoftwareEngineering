from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from controller import Controller

class MyFloatLayout(FloatLayout):
    toolbar_expanded = True  # Zustand der Toolbar

    def get_categories(self):
        return Controller.getAllCategories()

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

class WindowManager(ScreenManager):
    pass

class P(FloatLayout):
    pass

class FirstWindow(Screen, MyFloatLayout):
    def __init__(self, **kwargs):
        super(FirstWindow, self).__init__(**kwargs)
        self.cardList = []  # Initialize cardList here
        self.cardIndex = 0
        self.show_answer = False

    def getCardsForCategory(self):
        self.cardList = Controller.getAllCardsForCategory("Softwareentwicklung")

    def nextCard(self):
        if self.cardIndex < len(self.cardList):
            card = self.cardList[self.cardIndex]
            self.cardIndex += 1
            self.ids.learnmodeQuestion.text = card.question
            self.ids.learnmodeAnswer.text = "Antwort anzeigen"
            self.ids.learnmodeCategory.text = card.category
            self.show_answer = False
            # Hide rating buttons
            self.ids.ratingFalse.opacity = 0
            self.ids.ratingMiddle.opacity = 0
            self.ids.ratingGood.opacity = 0
        else:
            self.ids.learnmodeQuestion.text = "Das wars!"
            self.ids.learnmodeAnswer.text = "Du hast alle Karten der Kategorie gelernt!"
            self.ids.learnmodeCategory.text = "Herzlichen Glückwunsch!"

    def toggle_answer_visibility(self):
        if self.cardIndex > 0 and self.cardIndex <= len(self.cardList):
            if not self.show_answer:
                self.ids.learnmodeAnswer.text = self.cardList[self.cardIndex - 1].answer
                self.show_answer = True
                # Show rating buttons
                self.ids.ratingFalse.opacity = 1
                self.ids.ratingMiddle.opacity = 1
                self.ids.ratingGood.opacity = 1
            else:
                self.ids.learnmodeAnswer.text = "Antwort anzeigen"
                self.show_answer = False
                # Hide rating buttons
                self.ids.ratingFalse.opacity = 0
                self.ids.ratingMiddle.opacity = 0
                self.ids.ratingGood.opacity = 0

    def resetLearnmode(self):
        self.ids.learnmodeQuestion.text = "Frage"
        self.ids.learnmodeAnswer.text = "Antwort"
        self.ids.learnmodeCategory.text = "Kategorie"
        self.cardIndex = 0
        self.show_answer = False
        # Hide rating buttons
        self.ids.ratingFalse.opacity = 0
        self.ids.ratingMiddle.opacity = 0
        self.ids.ratingGood.opacity = 0

class SecondWindow(Screen):
    pass

class FirstApp(App):
    def build(self):
        kv = Builder.load_file('first_window.kv')
        return kv

if __name__ == "__main__":
    FirstApp().run()