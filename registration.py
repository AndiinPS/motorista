import bcrypt
import sqlite3
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import smtplib
from email.mime.text import MIMEText
from kivy.uix.boxlayout import BoxLayout
from dotenv import load_dotenv

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

    # Criando o hash da senha
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    c.execute("INSERT INTO users VALUES (?,?,?,?)", (name, email, birthdate, hashed_password))
    conn.commit()
    conn.close()

# Função para enviar e-mail de confirmação
def send_confirmation_email(email, name):
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

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

class RegistrationScreen(GridLayout):

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
        password_box = BoxLayout(orientation='horizontal')
        self.add_widget(Label(text='Senha'))
        self.password_input = TextInput(password=True, multiline=False)
        password_box.add_widget(self.password_input)

        self.toggle_button = Button(text='Ver')
        self.toggle_button.bind(on_press=self.toggle_password_visibility)
        password_box.add_widget(self.toggle_button)
        self.add_widget(password_box)

        # Botão para registrar
        self.register_button = Button(text='Registrar')
        self.register_button.bind(on_press=self.register_user)
        self.add_widget(self.register_button)

    def toggle_password_visibility(self, instance):
        if self.password_input.password:
            self.password_input.password = False
            self.toggle_button.text = 'Ocultar'
        else:
            self.password_input.password = True
            self.toggle_button.text = 'Ver'

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

        # Possivelmente limpar os campos do formulário aqui
        # e/ou redirecionar o usuário para outra tela

    def verify_password(user_password, stored_password):
        return bcrypt.checkpw(user_password.encode('utf-8'), stored_password)


class MyApp(App):

    def build(self):
        return RegistrationScreen()

if __name__ == '__main__':
    MyApp().run()
