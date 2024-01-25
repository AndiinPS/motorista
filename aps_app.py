from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
import requests

GOOGLE_API_KEY = 'AIzaSyCaUCyLGkWvCRKdlG8ITwK4WMRMVxtA9GQ'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Bem-vindo ao APS App!'))

        self.call_taxi_btn = Button(text='Calcular uma viagem')
        self.call_taxi_btn.bind(on_press=self.call_taxi)
        layout.add_widget(self.call_taxi_btn)

        self.history_btn = Button(text='Histórico de Corridas')
        self.history_btn.bind(on_press=self.view_history)
        layout.add_widget(self.history_btn)

        self.add_widget(layout)

    def call_taxi(self, instance):
        self.manager.current = 'calculate'

    def view_history(self, instance):
        print('Ver histórico de corridas!')

class CalculateScreen(Screen):
    def __init__(self, **kwargs):
        super(CalculateScreen, self).__init__(**kwargs)
        self.layout = GridLayout(cols=2)
        

        # Checkbox para local atual
        self.layout.add_widget(Label(text='Já está no local de embarque?'))
        self.current_location_checkbox = CheckBox(active=True)
        self.layout.add_widget(self.current_location_checkbox)
        self.current_location_checkbox.bind(active=self.on_checkbox_active)

        # Endereço de embarque
        self.layout.add_widget(Label(text='Endereço de Embarque'))
        self.start_address = TextInput(multiline=False)
        self.start_address.disabled = True
        self.layout.add_widget(self.start_address)

        # Endereço de destino
        self.layout.add_widget(Label(text='Endereço de Destino'))
        self.destination_address = TextInput(multiline=False)
        self.layout.add_widget(self.destination_address)

        # Checkbox e Input para Pedágio
        self.layout.add_widget(Label(text='Há pedágio no percurso?'))
        self.toll_checkbox = CheckBox(active=False)
        self.layout.add_widget(self.toll_checkbox)
        self.toll_checkbox.bind(active=self.on_toll_checkbox_active)

        self.layout.add_widget(Label(text='Valor do Pedágio'))
        self.toll_value = TextInput(multiline=False, input_type='number')
        self.toll_value.disabled = True
        self.layout.add_widget(self.toll_value)

        # Valor por km
        self.layout.add_widget(Label(text='Valor por KM'))
        self.value_per_km = TextInput(multiline=False, input_type='number')
        self.layout.add_widget(self.value_per_km)

        # Botão para calcular
        self.calculate_button = Button(text='Calcular')
        self.calculate_button.bind(on_press=self.calculate_fare)
        self.layout.add_widget(self.calculate_button)

        # Label para mostrar o resultado
        self.result = Label(text='')
        self.layout.add_widget(self.result)

        self.add_widget(self.layout)


    @staticmethod
    def is_valid_address(address):
        return address.strip() != ""

    @staticmethod
    def is_valid_number(value):
        try:
            num = float(value)
            return num >= 0  # ou outra lógica específica
        except ValueError:
            return False
        
    def calculate_fare(self, instance):
        # Validação dos dados de entrada
        if not self.is_valid_address(self.destination_address.text):
            self.result.text = 'Endereço de destino inválido!'
            return

        if not self.is_valid_number(self.value_per_km.text):
            self.result.text = 'Valor por KM inválido!'
            return

        if self.toll_checkbox.active and not self.is_valid_number(self.toll_value.text):
            self.result.text = 'Valor do pedágio inválido!'
            return

    




    def get_location_from_flask():
        response = requests.get('http://localhost:8080/get_location')  # Assumindo que a API Flask está rodando localmente

        if response.status_code == 200:
            location_data = response.json()
            latitude = location_data['location']['lat']
            longitude = location_data['location']['lng']
            print(f"Latitude: {latitude}\nLongitude: {longitude}")
        else:
            print("Não foi possível obter a localização. Status Code:", response.status_code)


    def process_fare_calculation(self, origin):
        destination = self.destination_address.text
        if not destination:
            self.result.text = 'Por favor, insira um endereço de destino!'
            return

        # Chamada para calcular a distância
        distance = self.calculate_distance_matrix(origin, destination)
        value_per_km = float(self.value_per_km.text)
        toll_value = float(self.toll_value.text) if self.toll_checkbox.active else 0

        # Cálculo da tarifa
        fare = distance * value_per_km + toll_value
        self.result.text = f'Tarifa estimada: R${fare:.2f}'

        
        
   
    
    def get_distance_from_flask(lat1, lon1, destination_address):
        params = {
        'lat1': lat1,
        'lon1': lon1,
        'destination': destination_address
    }
        response = requests.get('http://localhost:8080/calculate_distance', params=params)

        if response.status_code == 200:
            data = response.json()
            for item in data:
                print(f"Distância de {item['origem']} até {item['destino']}: {item['distância']}, tempo aproximado: {item['duração']}")
        else:
            print("Não foi possível calcular a distância. Status Code:", response.status_code)
        
   


    def get_address_from_location(self, lat, lng):
        """
        Converte latitude e longitude em um endereço.
        """
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key=AIzaSyCaUCyLGkWvCRKdlG8ITwK4WMRMVxtA9GQ"
        response = requests.get(geocode_url)
        if response.status_code == 200:
            results = response.json()['results']
            if results:
                return results[0]['formatted_address']
            else:
                return "Endereço não encontrado"
        else:
            return "Erro na obtenção do endereço"

    def on_checkbox_active(self, checkbox, value):
        if value:
            address = self.get_current_location()
            self.start_address.text = address
        self.start_address.disabled = value


    def on_toll_checkbox_active(self, checkbox, value):
        self.toll_value.disabled = not value

    def calculate_fare(self, instance):
        try:
            # Verificação de entrada
            if not self.value_per_km.text or (self.toll_checkbox.active and not self.toll_value.text):
                self.result.text = 'Por favor, preencha todos os campos necessários!'
                return

            if self.current_location_checkbox.active:
                self.get_current_location()
            else:
                self.process_fare_calculation(self.start_address.text)

        except Exception as e:
            self.result.text = f'Erro: {e}'

class APSApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CalculateScreen(name='calculate'))
        return sm

if __name__ == '__main__':
    APSApp().run()

