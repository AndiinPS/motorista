import requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

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

class TaxiApp(GridLayout):
    # ... [Seu código anterior para TaxiApp aqui] ...

    def calculate_fare(self, instance):
        # Aqui você pega os endereços do usuário
        start_address = self.start_address.text
        destination_address = self.destination_address.text
        chave_api = "SuaChaveDaAPI"

        # Chama a função para calcular a distância e duração
        resultado = calcular_distancia_duracao(start_address, destination_address, chave_api)

        if resultado:
            distancia, duracao = resultado
            self.result.text = f"Distância: {distancia}, Duração: {duracao}"
        else:
            self.result.text = "Não foi possível obter a distância."

class MyApp(App):
    def build(self):
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(TaxiApp())
        return scroll_view

if __name__ == '__main__':
    MyApp().run()



