import requests
import smtplib
from kivy.network.urlrequest import UrlRequest
import webbrowser
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
from email.mime.multipart import MIMEMultipart
import webbrowser
import json
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
import re


def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name TEXT, email TEXT, birthdate TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def add_user(name, email, birthdate, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?,?)", (name, email, birthdate, password))
        conn.commit()
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")
    finally:
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
    
def open_url_in_maps(start_address, destination_address):
    # Substitui espaços por '+' para URL encoding
    start_address = start_address.replace(' ', '+')
    destination_address = destination_address.replace(' ', '+')
    
    # Monta a URL
    url = f"https://www.google.com/maps/dir/{start_address}/{destination_address}"
    
    # Abre a URL no navegador padrão
    webbrowser.open(url)

def enviar_email(email, name):
    """
    Envia um e-mail de confirmação de cadastro.
    
    :param email: O endereço de e-mail do destinatário.
    :param name: O nome do destinatário.
    """
    # Configurações do servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Informações de autenticação
    email_usuario = 'andersonprogramador123@gmail.com'
    senha = 'l s t l k y e g j v h d j g k c'

    # Construir o e-mail
    remetente = email_usuario
    destinatario = email
    assunto = 'Confirmação de Cadastro'
    corpo_email = f"Olá {name}, seu cadastro foi concluído com sucesso!"

    # Criar um objeto MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # Adicionar o corpo ao e-mail
    msg.attach(MIMEText(corpo_email, 'plain'))

    try:
        # Criar uma conexão SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar conexão TLS
        server.login(email_usuario, senha)  # Fazer login no servidor SMTP
        server.sendmail(remetente, destinatario, msg.as_string())  # Enviar e-mail
        server.quit()  # Encerrar a conexão SMTP
        print("E-mail de confirmação enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail de confirmação: {e}")
    
class MainScreen(Screen):
    
    google_login_url = 'https://accounts.google.com/o/oauth2/auth'

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
        self.register_button.bind(on_press=self.on_register)
        layout.add_widget(self.register_button)

        self.add_widget(layout)

    def login(self, instance):
        self.manager.current = 'login'

    def google_login(self, instance):
        # Lógica para login com conta do Google
        params = {
            'response_type': 'token',
            'client_id': 'SEU_CLIENT_ID',
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'scope': 'email profile openid',
        }
        login_url = self.google_login_url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        webbrowser.open(login_url)

    def on_register(self, instance):
        self.manager.current = 'register'


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Login'))

        # Campos de usuário e senha
        self.add_widget(Label(text='Usuário'))
        self.username = TextInput(multiline=False, hint_text='Digite seu usuário')
        layout.add_widget(self.username)

        self.add_widget(Label(text='Senha'))
        self.password = TextInput(password=True, multiline=False, hint_text='Digite sua senha')
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
            # Adiciona uma mensagem de erro
            error_label = Label(text='Usuário ou senha inválidos. Tente novamente.')
            self.add_widget(error_label)
            self.manager.current = 'register'  # Redireciona para a tela de registro
            
    def on_register_pressed(self, instance):
        self.manager.current = 'register'  # Transição para a tela de registro

    def login_with_google(self, instance):
        # URL de login do Google
        google_login_url = 'https://accounts.google.com/o/oauth2/auth'
        
        # Parâmetros necessários para a solicitação de login
        params = {
            'response_type': 'token',
            'client_id': 'SEU_CLIENT_ID',
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'scope': 'email profile openid',
        }
        
        # Construindo a URL de login
        login_url = google_login_url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        
        # Abrindo a URL no navegador padrão
        webbrowser.open(login_url)

    def open_taxi_app(self):
        # Abrir a tela TaxiApp
        self.root.clear_widgets()
        self.root.add_widget(TaxiApp())
          
class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Registrando'))

        # Nome do usuário
        self.add_widget(Label(text='Nome Completo'))
        self.name_input = TextInput(multiline=False, hint_text='Digite seu nome completo')
        layout.add_widget(self.name_input)

        # E-mail
        self.add_widget(Label(text='E-mail'))
        self.email_input = TextInput(multiline=False, hint_text='Digite seu e-mail')
        layout.add_widget(self.email_input)

        # Data de nascimento
        self.add_widget(Label(text='Data de Nascimento'))
        self.birthdate_input = TextInput(multiline=False, hint_text='Digite sua data de nascimento')
        layout.add_widget(self.birthdate_input)

        # Senha
        password_box = BoxLayout(orientation='horizontal')
        self.add_widget(Label(text='Senha'))
        self.password_input = TextInput(password=True, multiline=False, hint_text='Digite sua senha')
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
        enviar_email(email, name)

        # Redireciona o usuário para a tela de login após o cadastro
        self.manager.current = 'login'

    def clear_form_fields(self):
        # Limpa os campos do formulário
        self.name_input.text = ''
        self.email_input.text = ''
        self.birthdate_input.text = ''
        self.password_input.text = ''

    def register(self, instance):
        self.manager.current = 'main'
        # Redireciona o usuário para outra tela (opcional)

class AutoCompleteTextInput(TextInput):
    def __init__(self, **kwargs):
        super(AutoCompleteTextInput, self).__init__(**kwargs)
        self.dropdown = None

    def on_text(self, instance, value):
        if len(value) > 3:  
            url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?key=AIzaSyCaUCyLGkWvCRKdlG8ITwK4WMRMVxtA9GQ&input={value}&types=establishment&region=br"
            UrlRequest(url, self.on_autocomplete_response)
        else:
            self.dismiss_dropdown()

    def on_autocomplete_response(self, request, response):
        if response['status'] == 'OK':
            predictions = response['predictions']
            addresses = [prediction['description'] for prediction in predictions]
            if not self.dropdown:
                self.create_dropdown(addresses)
            else:
                self.update_dropdown(addresses)

    def create_dropdown(self, addresses):
        self.dropdown = DropDown()
        for address in addresses:
            btn = Button(text=address, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.set_address(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.open(self)

    def update_dropdown(self, addresses):
        self.dropdown.clear_widgets()
        for address in addresses:
            btn = Button(text=address, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.set_address(btn.text))
            self.dropdown.add_widget(btn)

    def set_address(self, address):
        self.text = address
        self.dismiss_dropdown()

    def dismiss_dropdown(self):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None


from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.gridlayout import GridLayout

class TaxiApp(Screen):
    def __init__(self, **kwargs):
        super(TaxiApp, self).__init__(**kwargs)
        
        layout = AnchorLayout(anchor_x='center', anchor_y='center')
        main_layout = BoxLayout(orientation='vertical')
        
        main_layout.add_widget(Label(text='Para onde vamos?'))

        # Adicionando checkbox para indicar se o usuário já está no local de embarque
        main_layout.add_widget(Label(text='Já está no endereço de Embarque?'))
        self.current_location_checkbox = CheckBox(active=False)
        self.current_location_checkbox.bind(active=self.on_checkbox_active)  
        main_layout.add_widget(self.current_location_checkbox)

        # Adicionando campo de entrada com autocompletar para o endereço de embarque
        main_layout.add_widget(Label(text='Embarque:'))
        self.start_address_input = AutoCompleteTextInput(hint_text='Endereço de Embarque', size_hint=(.5, .5), height=25, pos_hint={"center_x":.5, "center_y":.65})
        main_layout.add_widget(self.start_address_input)

        # Adicionando layout para os endereços de parada e destino
        self.address_layout = BoxLayout(orientation='vertical', size_hint=(1, None))
        self.address_inputs_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.address_inputs_layout.bind(minimum_height=self.address_inputs_layout.setter('height'))
        self.address_inputs_layout.height = 0  # Inicialmente, o layout dos endereços de parada estará invisível
        self.address_layout.add_widget(self.address_inputs_layout)

        # Campo de entrada para o endereço de destino
        self.destination_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.destination_label = Label(text='Endereço de Destino:', size_hint=(1, None), height=30)
        self.destination_address_input = TextInput(hint_text='Endereço de Destino', size_hint=(1, None), height=40)
        self.add_address_button = Button(text='+', size_hint=(None, None), size=(40, 40))
        self.add_address_button.bind(on_press=self.add_address_field)
        self.destination_layout.add_widget(self.destination_label)
        self.destination_layout.add_widget(self.destination_address_input)
        self.destination_layout.add_widget(self.add_address_button)
        self.address_layout.add_widget(self.destination_layout)

        main_layout.add_widget(self.address_layout)
        # Adicionando checkbox para indicar se há pedágio
        main_layout.add_widget(Label(text='Tem Pedágio?'))
        self.toll_checkbox = CheckBox()
        self.toll_checkbox.bind(active=self.on_toll_checkbox_active)  
        main_layout.add_widget(self.toll_checkbox)

        # Campo de entrada para o valor do pedágio
        self.toll_value_label = Label(text='Valor do Pedágio:')
        main_layout.add_widget(self.toll_value_label)
        self.toll_value = TextInput(hint_text='R$ 0,00' , multiline=False, size_hint=(None,None), height=30, pos_hint={"center_x":.50, "center_y":.75})
        self.toll_value.bind(on_text_validate=self.validate_currency_input)
        main_layout.add_widget(self.toll_value)

       # Campo de entrada para o valor do quilômetro
        main_layout.add_widget(Label(text='Valor do KM:', size_hint=(None,None), height=30, pos_hint={"center_x":.50, "center_y":.75}))
        self.km_value = TextInput(hint_text='R$ 0,00', multiline=False,  size_hint=(None,None), height=30, pos_hint={"center_x":.50, "center_y":.75})
        self.km_value.bind(on_text=self.format_currency)
        main_layout.add_widget(self.km_value)

        # Botão para calcular a tarifa
        self.calculate_button = Button(text='Calcular Tarifa', size_hint=(.2,None), height=35, pos_hint={"center_x":.50, "center_y":.75})
        self.calculate_button.bind(on_press=self.calculate_fare)
        main_layout.add_widget(self.calculate_button)

        # Resultado do cálculo
        self.result = Label(text='')
        main_layout.add_widget(self.result)

        layout.add_widget(main_layout)
        self.add_widget(layout)

        self.toll_value_label.opacity = 0
        self.toll_value.opacity = 0

    def format_currency(self, instance, value):
        clean_value = re.sub(r'[^\d]', '', value)
        if clean_value == "":
            clean_value = "0"
        clean_value = int(clean_value)
        formatted_value = "R$ {:,.2f}".format(clean_value / 100).replace(',', 'v').replace('.', ',').replace('v', '.')
        instance.text = formatted_value
        instance.cursor = (len(formatted_value), 0)

    def validate_currency_input(self, instance):
        try:
            value_text = instance.text.replace("R$", "").strip()
            currency_value = float(value_text.replace(',', '.'))
            instance.text = f'R$ {currency_value:.2f}'.replace('.', ',')
        except ValueError:
            instance.text = "R$ 0,00"

    def add_address_field(self, instance):
    
    # Mostra o layout dos endereços de parada quando o botão "+" é pressionado
        self.address_inputs_layout.visible = True
    # Adiciona um novo campo de entrada para o endereço de parada
        if len(self.address_inputs_layout.children) < 5:  # Ajuste o limite conforme necessário
            address_input = AutoCompleteTextInput(hint_text='Endereço de Parada', size_hint=(0.5, 0.5), height=25, pos_hint={"center_x":.5, "center_y":.65})
            self.address_inputs_layout.add_widget(address_input)
        
        # Adiciona o botão "-" ao lado do novo campo de entrada
        remove_address_button = Button(text='-', size_hint=(None, None), size=(20, 20))
        remove_address_button.bind(on_press=lambda x: self.remove_address_field(address_input, remove_address_button))
        self.address_inputs_layout.add_widget(remove_address_button)
    # Se já houver 10 endereços, desabilita o botão de adicionar
        if len(self.address_inputs_layout.children) >= 5:
            instance.disabled = True


    def remove_address_field(self, address_input, remove_button):
        # Remove o campo de entrada e o botão "-" correspondente
        self.address_inputs_layout.remove_widget(address_input)
        self.address_inputs_layout.remove_widget(remove_button)
        
        # Habilita o botão de adicionar
        self.add_address_button.disabled = False

    def on_toll_checkbox_active(self, checkbox, value):
        self.toll_value_label.opacity = 1 if value else 0
        self.toll_value.opacity = 1 if value else 0

    def on_checkbox_active(self, checkbox, value):
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
                    self.start_address_input.text = endereco
                else:
                    print("Não foi possível obter o endereço.")
        else:
            # Se o checkbox não estiver marcado, permita que o usuário digite o endereço manualmente
            self.start_address_input.text = ""  # Limpa o texto do endereço de origem
            self.destination_address_input.text = ""  # Limpa o texto do endereço de destino

    def calculate_fare(self, instance):
        start_address = self.start_address_input.text
        destination_address = self.destination_address_input.text
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
            open_url_in_maps(start_address, destination_address)
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
        taxi_app_screen = TaxiApp(name='taxi_app')

        screen_manager.add_widget(main_screen)
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(register_screen)
        screen_manager.add_widget(taxi_app_screen)

        return screen_manager


if __name__ == '__main__':
    APSApp().run()