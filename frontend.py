from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.accordion import AccordionItem
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton
from kivy.uix.gridlayout import GridLayout
 
 
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
        popupWindow.open()
 
 
class P(FloatLayout):
    pass
 
 
class MyApp(App):
    def build(self):
        return MyFloatLayout()
 
 
if __name__ == "__main__":
    MyApp().run()