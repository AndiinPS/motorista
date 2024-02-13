from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

# Aqui você deve incluir as definições e funções adicionais necessárias

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Bem-vindo ao APS App!'))

        self.login_btn = Button(text='Login')
        self.login_btn.bind(on_press=self.login)
        layout.add_widget(self.login_btn)

        self.google_login_btn = Button(text='Login com Google')
        self.google_login_btn.bind(on_press=self.google_login)
        layout.add_widget(self.google_login_btn)

        self.register_btn = Button(text='Registrar')
        self.register_btn.bind(on_press=self.register)
        layout.add_widget(self.register_btn)

        self.add_widget(layout)

    def login(self, instance):
        self.manager.current = 'login'

    def google_login(self, instance):
        # Lógica para login com conta do Google
        print('Login com Google')

    def register(self, instance):
        self.manager.current = 'register'


class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=2)

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
        self.register_button = Button(text='R')
        self.register_button.bind(on_press=self.register_user)
        self.add_widget(self.register_button)

        self.add_widget(layout)

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
        # Adicione aqui a lógica para adicionar o usuário ao banco de dados

        # Envia o e-mail de confirmação
        # Adicione aqui a lógica para enviar o e-mail de confirmação

        # Possivelmente limpar os campos do formulário aqui
        # e/ou redirecionar o usuário para outra tela

    def verify_password(user_password, stored_password):
        # Adicione aqui a função para verificar a senha
        pass

    def register(self, instance):
        self.manager.current = 'register'


class APSApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(RegistrationScreen(name='register'))  # Adicionada a tela de registro
        return sm

if __name__ == '__main__':
    APSApp().run()