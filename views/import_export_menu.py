from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from controller.controller import Controller
from kivy.uix.label import Label

from tkinter import Tk, filedialog
from tkinter.filedialog import askopenfilename

from models.card.card import Card



class ImportExportPopUp():
    def show_popup(layout):
        # Layout für das Popup
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Platzhalter-Buttons
        label = Label(text="CSV-Dateien sind immer in dem Format Kategorie,Frage,Antwort", size_hint=(1, 0.3), color="white")
        import_button = Button(text="CSV-Import", size_hint=(1, 0.3), on_release=lambda instance: ImportExportPopUp.import_csv(layout, popup))
        export_button = Button(text="CSV-Export", size_hint=(1, 0.3), on_release=lambda instance: ImportExportPopUp.export_csv(layout))


        # Buttons dem Layout hinzufügen
        popup_layout.add_widget(label)
        popup_layout.add_widget(import_button)
        popup_layout.add_widget(export_button)

        # Popup erstellen
        popup = Popup(
            title="Aktion abgeschlossen",
            content=popup_layout,
            size_hint=(0.8, 0.5),
            auto_dismiss=True  # Schließt sich automatisch, wenn außerhalb des Popups geklickt wird
        )


 

        # Popup öffnen
        popup.open()
    
    def import_csv(layout, popup):



        root = Tk()
        root.withdraw()  # Versteckt das Hauptfenster von Tkinter
        root.attributes('-topmost', True)  # Bringt den Dialog in den Vordergrund

        # Datei auswählen
        file_path = askopenfilename(title="Datei auswählen", 
                                    filetypes=[("csv", "*.csv")])
        if file_path.endswith(".csv"):
            popup.dismiss()
            Controller.upload_csv(csv_path=file_path)
        ImportExportPopUp.reload_app(layout)


    def export_csv(layout):
    # "Speichern unter"-Dialog öffnen
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",  # Standarddateierweiterung
            filetypes=[
                ("CSV-Datei", "*.csv"),
                ("Alle Dateien", "*.*")
            ]
        )
        
        # Wenn ein Dateipfad gewählt wurde, die Datei speichern
        if file_path:
            csv_string = Controller.export_csv()
            with open(file_path, 'w', encoding="utf-8") as file:

                file.write(csv_string)  # Inhalt, der in die Datei geschrieben wird
            print(f"Datei gespeichert: {file_path}")
        ImportExportPopUp.reload_app(layout)

    def reload_app(layout):
        from views.frontend import BrainBoostFirstWindow
        layout.ids.folder_box.clear_widgets()
        layout.on_startup_create_all_folders()
        BrainBoostFirstWindow.resetLearnmode(layout)
