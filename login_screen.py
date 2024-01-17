import sqlite3
import requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import smtplib
from email.mime.text import MIMEText

# ... [Resto do seu código, como as definições de funções, etc.]
# Função para criar o banco de dados e a tabela de usuários
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name TEXT, email TEXT, birthdate TEXT, password TEXT)''')
    conn.commit()
    conn.close()

create_database()

# Função para adicionar um novo usuário ao banco de dados
def add_user(name, email, birthdate, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?,?)", (name, email, birthdate, password))
    conn.commit()
    conn.close()

# Função para enviar e-mail de confirmação
def send_confirmation_email(email, name):
    sender_email = "seuemail@gmail.com"  # Substitua pelo seu e-mail
    sender_password = "sua_senha"  # Substitua pela sua senha

    msg = MIMEText(f"Olá {name}, seu cadastro foi concluído com sucesso!")
    msg['Subject'] = "Confirmação de Cadastro"
    msg['From'] = sender_email
    msg['To'] = email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        # Campos de usuário e senha
        self.add_widget(Label(text='Nome de Usuário'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text='Senha'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        # Botões de login e registro
        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.on_login_pressed)
        self.add_widget(self.login_button)

        self.register_button = Button(text='Registrar Novo Usuário')
        self.register_button.bind(on_press=self.on_register_pressed)
        self.add_widget(self.register_button)

    def on_login_pressed(self, instance):
        # Aqui vai o código de verificação de login
        pass

    def on_register_pressed(self, instance):
        app = App.get_running_app()
        app.screen_manager.current = 'register'

class RegistrationScreen(GridLayout):
    # ... [Código da RegistrationScreen]
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        self.cols = 2

        # Nome do usuário
        self.add_widget(Label(text='Nome Completo'))
        self.name_input = TextInput(multiline=False)
        self.add_widget(self.name_input)

        # E-mail
        self.add_widget(Label(text='E-mail'))
        self.email_input = TextInput(multiline=False)
        self.add_widget(self.email_input)

        # Data de nascimento
        self.add_widget(Label(text='Data de Nascimento'))
        self.birthdate_input = TextInput(multiline=False)
        self.add_widget(self.birthdate_input)

        # Senha
        self.add_widget(Label(text='Senha'))
        self.password_input = TextInput(password=True, multiline=False)
        self.add_widget(self.password_input)

        # Botão para registrar
        self.register_button = Button(text='Registrar')
        self.register_button.bind(on_press=self.register_user)
        self.add_widget(self.register_button)

    def register_user(self, instance):
        # Supondo que você colete os dados do formulário aqui
        name = self.name_input.text
        email = self.email_input.text
        birthdate = self.birthdate_input.text
        password = self.password_input.text

        # Adiciona o usuário ao banco de dados
        add_user(name, email, birthdate, password)

        # Envia o e-mail de confirmação
        send_confirmation_email(email, name)


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Tela de login
        self.login_screen = LoginScreen()
        self.screen_manager.add_widget(Screen(name='login', children=[self.login_screen]))

        # Tela de registro
        self.registration_screen = RegistrationScreen()
        self.screen_manager.add_widget(Screen(name='register', children=[self.registration_screen]))

        return self.screen_manager

if __name__ == '__main__':
    MyApp().run()
