# Importiert die Hauptklasse der Kivy-App
from kivy.app import App

# Importiert String- und Objekt-Eigenschaften aus Kivy
from kivy.properties import StringProperty, ObjectProperty

# Importiert verschiedene Layouts und Widgets aus Kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
# Window-Modul wird importiert, aber ist auskommentiert, um möglicherweise Vollbild-Einstellungen zu ändern
# from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

# Importiert die Controller-Klasse, die vermutlich Logik oder Datenzugriff beinhaltet
from controller import Controller

# Erstellt eine benutzerdefinierte Klasse, die FloatLayout erweitert
class MyFloatLayout(FloatLayout):
    # Eine Klassenvariable, um die globale Kategorie zu speichern
    globalCategory = ""


    # Konstruktor der Klasse
    def __init__(self, **kwargs):
        super(MyFloatLayout, self).__init__(**kwargs)
        MyFloatLayout.globalCategory = Controller.getAllCardsForCategory("*")
        #### APP STARTET IN FULLSCREEN ####
        # Das Setzen des Fensters auf Vollbild ist auskommentiert
        # Window.fullscreen = 'auto'

    # Methode, die aufgerufen wird, nachdem das Kivy-Layout geladen wurde
    def on_kv_post(self, base_widget):
        self.on_startup_create_all_folders()

    # Klassenmethode, um alle Kategorien abzurufen
    @classmethod
    def get_categories(cls):
        allUniqueCategories = Controller.getAllCategories()
        return allUniqueCategories

    # Methode, um bei Start alle Ordner zu erstellen
    def on_startup_create_all_folders(self):
        for category in MyFloatLayout.get_categories():
            self.add_folder_to_toolbar(category)

    # Methode, um alle Karten für eine bestimmte Kategorie abzurufen
    def get_all_cards_for_category(self, category: str):
        FirstWindow.getCardsForCategory(category)

    # Zustandsvariable, ob die Toolbar erweitert ist oder nicht
    toolbar_expanded = True

    # Methode, um die Toolbar ein- und auszublenden
    def toggle_toolbar(self):
        button = self.ids.t_button
        toolbar = self.ids.toolbar
        icon = button.canvas.before.children[1]

        if self.toolbar_expanded:
            # Animation zum Ausblenden der Toolbar
            toolbar_anim = Animation(pos_hint={'x': -0.2}, duration=0.2)
            button_anim = Animation(pos_hint={'x': 0.00001}, duration=0.2)
            new_icon = 'ressources/right-arrow.png'
        else:
            # Animation zum Einblenden der Toolbar
            toolbar_anim = Animation(pos_hint={'x': 0}, duration=0.2)
            button_anim = Animation(pos_hint={'x': 0.2}, duration=0.2)
            new_icon = 'ressources/left-arrow.png'

        toolbar_anim.start(toolbar)
        button_anim.start(button)
        icon.source = new_icon

        # Zustand der Toolbar umschalten
        self.toolbar_expanded = not self.toolbar_expanded

    # Methode, die bei Klick auf einen Button aufgerufen wird
    def btn(self):
        self.show_popup()

    # Methode, um ein Popup anzuzeigen
    def show_popup(self):
        show = PopupAddCard()
        # Setzt die gewählte Kategorie in das Popup
        show.ids.questionCategory.text = MyFloatLayout.globalCategory
        popupWindow = Popup(title="Add Flashcard", content=show, size_hint=(None, None), size=(400, 400))

        # Methode zum Speichern der Daten im Popup
        def save_data(instance):
            value1 = show.ids.questionName.text
            value2 = show.ids.questionAnswer.text
            value3 = show.ids.questionCategory.text
            Controller.createCard(question=value1, answer=value2, category=value3)
            popupWindow.dismiss()

        show.ids.addCard.bind(on_release=save_data)
        popupWindow.open()

    # Methode, um ein weiteres Popup anzuzeigen
    def show_popuptoolbar(self):
        self.show_popup_folder()

    # Methode, um ein Popup für die Toolbar anzuzeigen
    def show_popup_folder(self):
        show = PopupToolbar(parent_widget=self)
        popupWindow = Popup(title="                 Ordner Erstellen", content=show, size_hint=(None, None), size=(250, 250),
                            pos_hint={'center_x': 0.17, 'center_y': 0.25})
        popupWindow.open()

    # Methode, um einen Ordner zur Toolbar hinzuzufügen
    def add_folder_to_toolbar(self, folder_name):
        # Erstellt ein neues Folder-Widget
        first_window = self.manager.get_screen('first_window')
        folder = Folder(folder_name=folder_name, first_window=first_window)
        self.ids.folder_box.add_widget(folder, index=0)

    # Methode, um einen Ordner auszuwählen
    def select_folder(self, instance):
        self.selected_folder = instance
        print(f"Selected folder: {instance.folder_name}")

    # Methode, um Text in einen Ordner zu verschieben
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


# Klasse für das Management der verschiedenen Fenster
class WindowManager(ScreenManager):
    pass


# Klasse für das Popup zum Hinzufügen einer Karte
class PopupAddCard(FloatLayout):
    def generate_answer(self):
        question = self.ids.questionName.text
        category = ""
        if self.ids.questionCategory.text != "":
            category = self.ids.questionCategory.text
        self.ids.questionAnswer.text = Controller.generate_answer(question=question, category=category)
    

# Klasse für das erste Fenster, das die Hauptseite darstellt
class FirstWindow(Screen, MyFloatLayout):
    eye_icon = StringProperty('ressources/eye-closed.png')  # Standardbild für geschlossenes Auge
    cardIndex = 0
    card = None

    # Konstruktor der Klasse
    def __init__(self, **kwargs):
        super(FirstWindow, self).__init__(**kwargs)
        self.get_all_cards_for_category("*")
        self.show_answer = False
        self.folder_instance = None

    # Methode, um die Instanz des Ordners zu setzen
    def set_folder_instance(self, folder_instance):
        self.folder_instance = folder_instance

    # Klassenmethode, um alle Karten für eine bestimmte Kategorie abzurufen
    @classmethod
    def getCardsForCategory(cls, category: str):
        FirstWindow.all_cards_list = Controller.getAllCardsForCategory(category)
        print("Alle Karten ", len(FirstWindow.all_cards_list))
        FirstWindow.cardList = []

    # Methode, um die nächste Karte anzuzeigen
    def nextCard(self):
        if not hasattr(self, 'cardList'):
            return
        if self.cardIndex < len(FirstWindow.cardList):
            FirstWindow.restart = False
            FirstWindow.card = self.cardList[self.cardIndex]
            self.cardIndex += 1
            self.ids.learnmodeQuestion.text = FirstWindow.card.question
            self.ids.learnmodeAnswer.text = ""
            self.ids.learnmodeCategory.text = FirstWindow.card.category
            self.show_answer = False
            self.ids.toggle_image.source = "ressources/eye-closed.png"
            self.ids.toggle_eye_label.text = "Antwort anzeigen"
            # Versteckt die Bewertungsbuttons
            self.ids.ratingFalse.opacity = 0
            self.ids.ratingMiddle.opacity = 0
            self.ids.ratingGood.opacity = 0
        else:
            FirstWindow.restart = True
            self.ids.learnmodeQuestion.text = "Das wars!"
            self.ids.learnmodeAnswer.text = "Du hast alle Karten der Kategorie gelernt!"
            self.ids.learnmodeCategory.text = "Herzlichen Glückwunsch!"
        self.ids.cards_left.text = str(len(FirstWindow.cardList))

    def open_all_container(self):
        for i in range(1, 5):  # Hier gehe ich davon aus, dass du 4 Buttons hast wie in deiner .kv Datei
            button_id = f"kartei_{i}"  # Generiere die Button ID dynamisch
            image_button = self.ids[button_id]  # Zugriff auf das Button Widget über die ID
            
            # Zugriff auf das Image Widget innerhalb des Buttons und Aktualisierung der Bildquelle
            image_widget = image_button.children[0]  # Angenommen das Image ist das erste Kind
            image_widget.source = "box_open.png"  # Setze die neue Bildquelle
        self.start_container_mode()    

            


    # Methode, um die aktuelle Karte als bekannt zu markieren und die nächste Karte anzuzeigen
    def set_card_one_container_up(self):
        if FirstWindow.card.container_number != 1:
            FirstWindow.card.container_number -= 1 
        Controller.set_card_on_container_up(FirstWindow.card)
        self.nextCard()

    # Methode, um die aktuelle Karte als unbekannt zu markieren und die nächste Karte anzuzeigen
    def set_card_one_container_down(self):
        if FirstWindow.card.container_number != 4:
            FirstWindow.card.container_number += 1 
        Controller.set_card_on_container_down(FirstWindow.card)
        self.nextCard()

    def add_filter_number(self, filter_number):
        self.start_len = len(FirstWindow.cardList)
        FirstWindow.cardList.extend(Controller.add_cards_to_filtered_cards(filter_number, FirstWindow.all_cards_list))
        #FirstWindow.cardList
        self.final_len = len(FirstWindow.cardList)
        
        print(len(FirstWindow.cardList))

    def start_container_mode(self):
        self.ids.cards_left.text = str(len(FirstWindow.all_cards_list))
        for i in range (1,5):
            self.add_filter_number(i)

    def del_filter_number(self, filter_number):
        filtered_ids = Controller.del_cards_in_filtered_cards(filter_number, FirstWindow.cardList)
        original_length = len(FirstWindow.cardList)
        FirstWindow.cardList[:] = [elem for elem in FirstWindow.cardList if elem.cardID not in filtered_ids]
        print(f"Removed {original_length - len(FirstWindow.cardList)} cards for filter number {filter_number}")
        print(f"Total cards in cardList after removing: {len(FirstWindow.cardList)}")
        self.final_len = 0  
        self.start_len = 0



    def toggle_answer_visibility(self):
        if len(FirstWindow.cardList) != 0:
            if not self.show_answer:
                self.ids.learnmodeAnswer.text = FirstWindow.card.answer
                self.show_answer = True
                # Zeigt die Bewertungsbuttons
                self.ids.ratingFalse.opacity = 1
                self.ids.ratingMiddle.opacity = 1
                self.ids.ratingGood.opacity = 1
                # Ändert das Icon zu offenem Auge
                self.ids.toggle_image.source = "ressources/eye-open.png"
                self.ids.toggle_eye_label.text = "Antwort verbergen"
            else:
                self.ids.learnmodeAnswer.text = ""
                self.show_answer = False
                # Versteckt die Bewertungsbuttons
                self.ids.ratingFalse.opacity = 0
                self.ids.ratingMiddle.opacity = 0
                self.ids.ratingGood.opacity = 0
                # Ändert das Icon zu geschlossenem Auge
                self.ids.toggle_image.source = "ressources/eye-closed.png"
                self.ids.toggle_eye_label.text = "Antwort anzeigen"

    # Methode, um den Lernmodus zurückzusetzen
    def resetLearnmode(self):
        self.ids.learnmodeQuestion.text = "Frage"
        self.ids.learnmodeAnswer.text = ""
        self.ids.learnmodeCategory.text = "Kategorie"
        self.cardIndex = 0
        self.show_answer = False
        # Versteckt die Bewertungsbuttons
        self.ids.ratingFalse.opacity = 0
        self.ids.ratingMiddle.opacity = 0
        self.ids.ratingGood.opacity = 0
        self.ids.cards_left.text = ""

    def change_image(self, instance, id):
        image_widget = instance.children[0]  # The Image widget is a child of the Button
        try:
            if image_widget.source == "box_open.png":
                image_widget.source = 'box_closed.png'
                self.del_filter_number(id)
                
            else:
                image_widget.source = 'box_open.png'
                self.add_filter_number(id)

            self.ids.cards_left.text = str(len(FirstWindow.cardList))
        except:
            pass
        if FirstWindow.card not in FirstWindow.cardList:
            self.nextCard()
            print(len(FirstWindow.cardList))
            if len(FirstWindow.cardList) == 1:
                self.ids.learnmodeQuestion.text = FirstWindow.card.question
                self.ids.learnmodeAnswer.text = ""
                self.ids.learnmodeCategory.text = FirstWindow.card.category
                self.show_answer = False
                self.ids.toggle_image.source = "ressources/eye-closed.png"
                self.ids.toggle_eye_label.text = "Antwort anzeigen"
            self.cardIndex = 0
        if self.final_len > self.start_len and self.start_len == 0:
            self.nextCard()
            
        image_widget.reload()




# Klasse für das Popup der Toolbar
class PopupToolbar(FloatLayout):
    folder_name_input = ObjectProperty(None)

    def __init__(self, parent_widget, **kwargs):
        super(PopupToolbar, self).__init__(**kwargs)
        self.parent_widget = parent_widget

    # Methode, um einen neuen Ordner zu erstellen
    def create_folder(self, folder_name):
        if folder_name:
            self.parent_widget.add_folder_to_toolbar(folder_name)
        else:
            print("No folder name provided.")


# Klasse für die Ordner
class Folder(BoxLayout):
    folder_name = StringProperty("")
    first_window = ObjectProperty(None)
    last_folder = None

    def __init__(self, folder_name, first_window:FirstWindow, **kwargs):
        super(Folder, self).__init__(**kwargs)
        self.folder_name = folder_name
        self.first_window = first_window
        self.first_window.open_all_container()
        self.first_window.nextCard()

    # Methode, um Inhalte zum Ordner hinzuzufügen
    def add_content(self, content):
        self.ids.content.add_widget(Label(text=content, size_hint_y=None, height=30))

    # Methode, um das Ordner-Icon zu ändern
    def change_icon_folder(self):
        # Die Icons sollen sich abwechseln
        self.close_last_folder()
        current_icon = self.ids.folder_icon.source
        new_icon = 'folder.png' if current_icon == 'folderclosed.png' else 'folderclosed.png'
        self.ids.folder_icon.source = new_icon
        Folder.last_folder = self

    # Methode, um das Icon des letzten geöffneten Ordners zu schließen
    def close_last_folder(self):
        if Folder.last_folder != None:
            Folder.last_folder.ids.folder_icon.source = 'folderclosed.png'

    # Methode, um beim Klick auf einen Ordner die Karteninhalte zu löschen
    def reset_cards(self):
        if self.first_window:
            self.first_window.resetLearnmode()
        else:
            print("FirstWindow instance not set.")

    # In der Folder Klasse
    def get_all_cards_for_category(self, category: str):
        MyFloatLayout.globalCategory = category
        self.first_window.get_all_cards_for_category(category)
        self.first_window.open_all_container()
        #self.first_window.nextCard()


# Klasse für das zweite Fenster
class SecondWindow(Screen):
    pass

#--------- USER LOGIN --------------------

# Hauptklasse der Anwendung
class FirstApp(App):
    def build(self):
        # Lädt die Kivy-Datei, die das Layout definiert
        kv = Builder.load_file('first_window.kv')
        self.icon = 'dausb.jpg'
        return kv
    

class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def verify_credentials(self):
        user = self.username.text
        pwd = self.password.text
        verfified, userid = Controller.verify_credentials(user, pwd)
        if verfified:
            Controller.create_user(user, pwd, userid)
            LoginApp().stop()
            FirstApp().run()
        else:
            self.ids.message.color = "red"
            self.ids.message.text = "Invalid username or password"
            self.username.text = ""
            self.password.text = ""
    def register_user(self):
        user = self.username.text
        pwd = self.password.text
        if user != "" != pwd:
            Controller.register_user(user,pwd)
            self.ids.message.color = "green"
            self.ids.message.text = "Now, login!"
        else:
            self.ids.message.color = "red"
            self.ids.message.text = "Username and/or password are missing"

class WelcomeScreen(Screen):
    pass

class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        Builder.load_file('userlogin.kv')
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(WelcomeScreen(name='welcome'))
        return sm




# Startet die Anwendung
if __name__ == "__main__":
    LoginApp().run()
