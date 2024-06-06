from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from controller import Controller
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import StringProperty

class MyFloatLayout(FloatLayout):
    cardIndex = 0
    cardList = Controller.getAllCardsForCategory("Softwareentwicklung")
    # dropdown for categories
    dropdown = DropDown()
    
    def create_dropdown(self):
        # get all categories from database
        categories = Controller.getAllCategories() 
        for category in categories:
            # create buttons
            btn = Button(text=category, size_hint_y=None, height=44)
            print(btn)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            # place button
            self.dropdown.add_widget(btn)
    
    # when button with category is clicked
    def select_category(self, category):
        cardList = Controller.getAllCardsForCategory(category=category)
        self.ids.mainbutton.text = category

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

    def nextCard(self):
        if self.cardIndex < len(self.cardList):
            card = self.cardList[self.cardIndex]
            self.cardIndex += 1
            self.ids.question_label.text = card.question
            self.ids.answer_label.text = card.answer
            #self.ids.category_label.text = card.category
        else:
            self.ids.question_label.text = "Das wars!"
            self.ids.answer_label.text = "Du hast alle Karten der Kategorie gelernt!"
            self.ids.category_label.text = "Herzlichen Glückwunsch!"

class P(FloatLayout):
    pass

class MyApp(App):
    def build(self):
        return MyFloatLayout()


if __name__ == "__main__":
    Builder.load_file('my.kv')
    MyApp().run()
