from kivy.app import App
from registration import RegistrationScreen
from login_screen import LoginScreen
# Importe outras telas conforme necessário

class MyApp(App):
    def build(self):
        # Aqui você pode gerenciar qual tela mostrar primeiro,
        # por exemplo, RegistrationScreen ou LoginScreen
        return RegistrationScreen()

if __name__ == '__main__':
    MyApp().run()
