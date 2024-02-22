import requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
import sqlite3
from kivy.clock import Clock
import smtplib
from email.mime.text import MIMEText
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name TEXT, email TEXT, birthdate TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def add_user(name, email, birthdate, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?,?)", (name, email, birthdate, password))
    conn.commit()
    conn.close()

def verify_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def calcular_distancia_duracao(endereco_origem, endereco_destino, chave_api):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={endereco_origem}&destinations={endereco_destino}&key={chave_api}"

    try:
        response = requests.get(url)
        data = response.json()

        distance = data['rows'][0]['elements'][0]['distance']['text']
        duration = data['rows'][0]['elements'][0]['duration']['text']

        return distance, duration
    except Exception as e:
        print(f"Erro ao calcular distância: {e}")
        return None

def obter_localizacao_atual(chave_api):
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={chave_api}"

    try:
        response = requests.post(url)
        data = response.json()

        if 'location' in data:
            latitude = data['location']['lat']
            longitude = data['location']['lng']
            return latitude, longitude
        else:
            print("Não foi possível obter a localização atual.")
            return None
    except Exception as e:
        print(f"Erro ao obter a localização atual: {e}")
        return None

def obter_endereco(latitude, longitude, chave_api):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={chave_api}"

    try:
        response = requests.get(url)
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            endereco = data['results'][0]['formatted_address']
            return endereco
        else:
            print("Não foi possível obter o endereço.")
            return None
    except Exception as e:
        print(f"Erro ao obter o endereço: {e}")
        return None
    
def send_confirmation_email(email, name):
    creds, _ = google.auth.default()

    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(f"Olá {name}, seu cadastro foi concluído com sucesso!")

        message["To"] = email
        message["From"] = "andiinps@gmail.com"  # Substitua pelo seu e-mail
        message["Subject"] = "Confirmação de Cadastro"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"Erro ao enviar e-mail: {error}")
        send_message = None
    return send_message   
    
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Bem-vindo ao APS App!'))

        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.login)
        layout.add_widget(self.login_button)

        self.google_login_button = Button(text='Login com conta google')
        self.google_login_button.bind(on_press=self.google_login)
        layout.add_widget(self.google_login_button)

        self.register_button = Button(text='Registrar')
        self.register_button.bind(on_press=self.register)
        layout.add_widget(self.register_button)

        self.add_widget(layout)

    def login(self, instance):
        self.manager.current = 'login'

    def google_login(self, instance):
        # Lógica para login com conta do Google
        print('Login com Google')

    def register(self, instance):
        self.manager.current = 'register'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Tela de Login'))

        # Campos de usuário e senha
        self.add_widget(Label(text='Nome de Usuário'))
        self.username = TextInput(multiline=False)
        layout.add_widget(self.username)

        self.add_widget(Label(text='Senha'))
        self.password = TextInput(password=True, multiline=False)
        layout.add_widget(self.password)

        # Botões de login e registro
        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.on_login_pressed)
        layout.add_widget(self.login_button)

        self.register_button = Button(text='Registrar Novo Usuário')
        self.register_button.bind(on_press=self.on_register_pressed)
        layout.add_widget(self.register_button)

        self.add_widget(layout)

    def on_login_pressed(self, instance):
        username = self.username.text
        password = self.password.text

        # Verifica se o usuário está cadastrado
        if verify_login(username, password):
            self.manager.current = 'taxi_app'  # Se estiver cadastrado, abre a tela TaxiApp
        else:
            # Se não estiver cadastrado, exibe uma mensagem
            self.username.text = ''  # Limpa os campos de entrada
            self.password.text = ''
            self.manager.current = 'register'  # Redireciona para a tela de registro
            

    def on_register_pressed(self, instance):
        app = App.get_running_app()
        app.root.current = 'register'  # Ajustado para 'app.root.current' para acessar o ScreenManager
        
class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Tela de Registro'))

        # Nome do usuário
        self.add_widget(Label(text='Nome Completo'))
        self.name_input = TextInput(multiline=False)
        layout.add_widget(self.name_input)

        # E-mail
        self.add_widget(Label(text='E-mail'))
        self.email_input = TextInput(multiline=False)
        layout.add_widget(self.email_input)

        # Data de nascimento
        self.add_widget(Label(text='Data de Nascimento'))
        self.birthdate_input = TextInput(multiline=False)
        layout.add_widget(self.birthdate_input)

        # Senha
        password_box = BoxLayout(orientation='horizontal')
        self.add_widget(Label(text='Senha'))
        self.password_input = TextInput(password=True, multiline=False)
        password_box.add_widget(self.password_input)

        self.toggle_button = Button(text='Ver')
        self.toggle_button.bind(on_press=self.toggle_password_visibility)
        password_box.add_widget(self.toggle_button)
        layout.add_widget(password_box)

        # Botão para registrar
        self.register_button = Button(text='Registrar')
        self.register_button.bind(on_press=self.register_user)
        layout.add_widget(self.register_button)

        self.add_widget(layout)

    def toggle_password_visibility(self, instance):
        if self.password_input.password:
            self.password_input.password = False
            self.toggle_button.text = 'Ocultar'
        else:
            self.password_input.password = True
            self.toggle_button.text = 'Ver'

    def register_user(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        birthdate = self.birthdate_input.text
        password = self.password_input.text

        # Adiciona o usuário ao banco de dados
        add_user(name, email, birthdate, password)

        # Envia o e-mail de confirmação
        send_confirmation_email(email, name)

    def clear_form_fields(self):
        # Limpa os campos do formulário
        self.name_input.text = ''
        self.email_input.text = ''
        self.birthdate_input.text = ''
        self.password_input.text = ''

    def register(self, instance):
        self.manager.current = 'main'
        # Redireciona o usuário para outra tela (opcional)

class TaxiApp(GridLayout):
    def __init__(self, **kwargs):
        super(TaxiApp, self).__init__(**kwargs)
        self.cols = 2

        # Adicionando checkbox para indicar se o usuário já está no local de embarque
        self.add_widget(Label(text='Já está no local de embarque?'))
        self.current_location_checkbox = CheckBox(active=False)
        self.current_location_checkbox.bind(active=self.on_checkbox_active)  
        self.add_widget(self.current_location_checkbox)

        self.add_widget(Label(text='Endereço de Origem:'))
        self.start_address = TextInput(multiline=True)
        self.start_address.disabled = False
        self.add_widget(self.start_address)

        self.add_widget(Label(text='Endereço de Destino:'))
        self.destination_address = TextInput(multiline=False)
        self.add_widget(self.destination_address)

        self.add_widget(Label(text='Incluir Pedágio:'))
        self.toll_checkbox = CheckBox()
        self.toll_checkbox.bind(active=self.on_toll_checkbox_active)  
        self.add_widget(self.toll_checkbox)

        self.toll_value_label = Label(text='Valor do Pedágio:')
        self.add_widget(self.toll_value_label)
        self.toll_value = TextInput(multiline=False)
        self.add_widget(self.toll_value)

        self.add_widget(Label(text='Valor do KM:'))  # Adicionando rótulo para o campo de valor do km
        self.km_value = TextInput(multiline=False)  # Adicionando campo de valor do km
        self.add_widget(self.km_value)


        self.calculate_button = Button(text='Calcular Tarifa')
        self.calculate_button.bind(on_press=self.calculate_fare)
        self.add_widget(self.calculate_button)

        self.result = Label(text='')
        self.add_widget(self.result)

        self.toll_value_label.opacity = 0
        self.toll_value.opacity = 0

    def on_toll_checkbox_active(self, checkbox, value):
        self.toll_value_label.opacity = 1 if value else 0
        self.toll_value.opacity = 1 if value else 0

    def on_checkbox_active(self, checkbox, value):
        localizacao = None  # Inicializa localizacao com None
        if value:
       # Se o checkbox estiver marcado, puxe a localização atual
            chave_api = "AIzaSyCaUCyLGkWvCRKdlG8ITwK4WMRMVxtA9GQ"  # Substitua pela sua chave API do Google
            localizacao = obter_localizacao_atual(chave_api)
            if localizacao:  # Verifica se localizacao é diferente de None dentro do bloco onde é definido
                latitude, longitude = localizacao
            # Obter o endereço correspondente às coordenadas de latitude e longitude
                endereco = obter_endereco(latitude, longitude, chave_api)
                if endereco:
                # Preencher o campo de Endereço de Origem com o endereço obtido
                    self.start_address.text = endereco
                else:
                    print("Não foi possível obter o endereço.")
        else:
        # Se o checkbox não estiver marcado, permita que o usuário digite o endereço manualmente
            self.start_address.text = ""  # Limpa o texto do endereço de origem
            self.destination_address.text = ""  # Limpa o texto do endereço de destino

    def calculate_fare(self, instance):
        start_address = self.start_address.text
        destination_address = self.destination_address.text
        chave_api = "AIzaSyCaUCyLGkWvCRKdlG8ITwK4WMRMVxtA9GQ"

        if self.toll_checkbox.active:
            if self.toll_value.text:
                pedagio = float(self.toll_value.text)
            else:
                self.result.text = "Por favor, forneça o valor do pedágio."
                return
        else:
            pedagio = 0

        # Obtém o valor do km fornecido pelo usuário
        if self.km_value.text:
            valor_por_km = float(self.km_value.text)
        else:
            self.result.text = "Por favor, forneça o valor do quilômetro."
            return

        resultado = calcular_distancia_duracao(start_address, destination_address, chave_api)

        if resultado:
            distancia, duracao = resultado
            tarifa = self.calcular_tarifa(distancia, pedagio, valor_por_km)  # Passa o valor do km como parâmetro
            self.result.text = f"Distância: {distancia}, Duração: {duracao}, Tarifa Estimada: {tarifa}"
        else:
            self.result.text = "Não foi possível obter a distância."

    def calcular_tarifa(self, distancia, pedagio, valor_por_km):
        distancia_km = float(distancia.replace(',', '.').split()[0])
        tarifa = distancia_km * valor_por_km + pedagio
        return tarifa

class APSApp(App):
    def build(self):
        screen_manager = ScreenManager()

        main_screen = MainScreen(name='main')
        login_screen = LoginScreen(name='login')
        register_screen = RegistrationScreen(name='register')

        screen_manager.add_widget(main_screen)
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(register_screen)

        return screen_manager

if __name__ == '__main__':
    APSApp().run()
