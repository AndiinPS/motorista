import sqlite3
import requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class LoginScreen(GridLayout):
# Função para verificar o login
    def verify_login(username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        return user is not None


    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Nome'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='Senha'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.on_login_pressed)
        self.add_widget(self.login_button)

    def on_login_pressed(self, instance):
        username = self.username.text
        password = self.password.text
        dados_login = {'username': username, 'password': password}  # Definindo os dados de login
        resposta = requests.post('http://localhost:8080/login', json=dados_login)
        if resposta.status_code == 200:
            print("Login bem-sucedido!")
        else:
            print("Nome de usuário ou senha incorretos.")

class MyApp(App):

    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()
