from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from frontend import *
from controller import Controller

# Benutzerdatenbank (nur zum Beispiel)


class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def verify_credentials(self):
        user = self.username.text
        pwd = self.password.text
        verfified, userid = Controller.verify_credentials(user, pwd)
        if verfified:
            self.manager.current = 'welcome'
        else:
            self.ids.message.text = "Invalid username or password"
            self.username.text = ""
            self.password.text = ""

class WelcomeScreen(Screen):
    pass

class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        Builder.load_file('userlogin.kv')
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(WelcomeScreen(name='welcome'))
        return sm



