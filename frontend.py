from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

from controller import Controller


class MyFloatLayout(FloatLayout):
    toolbar_expanded = True  # Zustand der Toolbar

    # def on_kv_post(self, *args):
    # self.add_category_buttons()

    #def add_category_buttons(self):
    #categories = self.get_categories()
    #toolbar = self.ids.category_box
    #toolbar.clear_widgets()

    # for category in categories:
    # btn = Button(text=category, size_hint_y=None, height=40,
    #    on_release=lambda *args: self.get_all_cards_for_category(category))
    #toolbar.add_widget(btn)

    def get_categories(self):
        return Controller.getAllCategories()

    def get_all_cards_for_category(self, category: str):
        FirstWindow.getCardsForCategory(category)

    def toggle_toolbar(self):
        button = self.ids.t_button
        toolbar = self.ids.toolbar

        if self.toolbar_expanded:
            # Animation zum Ausblenden der Toolbar
            toolbar_anim = Animation(pos_hint={'x': -0.2}, duration=0.2)
            button_anim = Animation(pos_hint={'x': 0.01}, duration=0.2)
        else:
            # Animation zum Einblenden der Toolbar
            toolbar_anim = Animation(pos_hint={'x': 0}, duration=0.2)
            button_anim = Animation(pos_hint={'x': 0.2}, duration=0.2)

        toolbar_anim.start(toolbar)
        button_anim.start(button)
        self.toolbar_expanded = not self.toolbar_expanded

    def btn(self):
        self.show_popup()

    def show_popup(self):
        show = PopupAddCard()
        popupWindow = Popup(title="Add Flashcard", content=show, size_hint=(None, None), size=(400, 400))

        def save_data(instance):
            value1 = show.ids.questionName.text
            value2 = show.ids.questionAnswer.text
            value3 = show.ids.questionCategory.text
            Controller.createCard(question=value1, answer=value2, category=value3)
            popupWindow.dismiss()

        show.ids.addCard.bind(on_release=save_data)
        popupWindow.open()

    def show_popuptoolbar(self):
        self.show_popup_folder()

    def show_popup_folder(self):
        show = PopupToolbar(parent_widget=self)
        popupWindow = Popup(title="Add Folder", content=show, size_hint=(None, None), size=(200, 200),
                            pos_hint={'center_x': 0.1, 'center_y': 0.2})
        popupWindow.open()

    def add_folder_to_toolbar(self, folder_name):
        # Neues Folder-Widget erstellen
        folder = Folder(folder_name=folder_name)
        self.ids.folder_box.add_widget(folder, index=0)


    def add_content_to_folder(self, folder_name, content):
        for folder in self.ids.folder_box.children:
            if isinstance(folder, Folder) and folder.folder_name == folder_name:
                folder.add_content(content)
                break

    def select_folder(self, instance):
        self.selected_folder = instance
        print(f"Selected folder: {instance.folder_name}")

    def move_text_to_folder(self):
        if self.selected_folder:
            text = self.ids.text_input.text
            if text:
                self.selected_folder.add_content(text)
                self.ids.text_input.text = ''
            else:
                print("No text to move")
        else:
            print("No folder selected")


class WindowManager(ScreenManager):
    pass


class PopupAddCard(FloatLayout):
    pass


class FirstWindow(Screen, MyFloatLayout):
    cardIndex = 0

    def __init__(self, **kwargs):
        super(FirstWindow, self).__init__(**kwargs)
        # Initialize cardList here
        self.show_answer = False
        # self.add_category_buttons()

    @classmethod
    def getCardsForCategory(cls, category: str):
        FirstWindow.cardList = Controller.getAllCardsForCategory(category)

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


class PopupToolbar(FloatLayout):
    folder_name_input = ObjectProperty(None)

    def __init__(self, parent_widget, **kwargs):
        super(PopupToolbar, self).__init__(**kwargs)
        self.parent_widget = parent_widget

    def create_folder(self):
        folder_name = self.folder_name_input.text
        if folder_name:
            self.parent_widget.add_folder_to_toolbar(folder_name)
            self.folder_name_input.text = ''
        else:
            print("No folder name provided.")


class Folder(BoxLayout):
    folder_name = StringProperty("")

    def __init__(self, folder_name, **kwargs):
        super(Folder, self).__init__(**kwargs)
        self.folder_name = folder_name

    def add_content(self, content):
        self.ids.content.add_widget(Label(text=content, size_hint_y=None, height=30))

    def change_icon(self):
        # Die Icons sollen sich abwechseln
        current_icon = self.ids.folder_icon.source
        new_icon = 'folder.png' if current_icon == 'folderclosed.png' else 'folderclosed.png'
        self.ids.folder_icon.source = new_icon


class SecondWindow(Screen):
    pass


class FirstApp(App):
    def build(self):
        kv = Builder.load_file('first_window.kv')
        return kv


if __name__ == "__main__":
    FirstApp().run()
