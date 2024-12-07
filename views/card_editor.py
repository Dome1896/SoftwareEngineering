from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class TableRow(BoxLayout):
    """Eine Zeile in der Tabelle"""
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        for item in data:
            self.add_widget(Label(text=item, size_hint_x=0.3, halign="center"))

class TableView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{"viewclass": "TableRow", "data": row} for row in [
            ["Name", "Alter", "Beruf"],  # Überschriften
            ["Alice", "25", "Ingenieurin"],
            ["Bob", "30", "Designer"],
            ["Charlie", "35", "Manager"]
        ]]

class EditorApp(App):
    def build(self):
        return TableView()

