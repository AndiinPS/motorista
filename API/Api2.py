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
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(TaxiApp())
        return scroll_view

if __name__ == '__main__':
    APSApp().run()
