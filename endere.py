from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class TaxiApp(GridLayout):

    def __init__(self, **kwargs):
        super(TaxiApp, self).__init__(**kwargs)
        self.cols = 2

        # Checkbox para local atual
        self.add_widget(Label(text='Já está no local de embarque?'))
        self.current_location_checkbox = CheckBox(active=True)
        self.add_widget(self.current_location_checkbox)
        self.current_location_checkbox.bind(active=self.on_checkbox_active)  # Evento adicionado

        # endereço de embarque
        self.add_widget(Label(text='Endereço de Embarque'))
        self.start_address = TextInput(multiline=False)
        self.start_address.disabled = True  # Desabilitado por padrão
        self.add_widget(self.start_address)


        # Endereço de destino
        self.add_widget(Label(text='Endereço de Destino'))
        self.destination_address = TextInput(multiline=False)
        self.add_widget(self.destination_address)


         # Checkbox e Input para Pedágio
        self.add_widget(Label(text='Há pedágio no percurso?'))
        self.toll_checkbox = CheckBox(active=False)
        self.add_widget(self.toll_checkbox)
        self.toll_checkbox.bind(active=self.on_toll_checkbox_active)

        self.add_widget(Label(text='Valor do Pedágio'))
        self.toll_value = TextInput(multiline=False, input_type='number')
        self.toll_value.disabled = True  # Desabilitado por padrão
        self.add_widget(self.toll_value)

        # Valor por km
        self.add_widget(Label(text='Valor por KM'))
        self.value_per_km = TextInput(multiline=False, input_type='number')
        self.add_widget(self.value_per_km)

        # Botão para calcular
        self.calculate_button = Button(text='Calcular')
        self.calculate_button.bind(on_press=self.calculate_fare)
        self.add_widget(self.calculate_button)

        # Label para mostrar o resultado
        self.result = Label(text='')
        self.add_widget(self.result)
        
    def on_checkbox_active(self, checkbox, value):
        # Habilita ou desabilita a entrada de KM até o Embarque
            self.start_address.disabled = value

    def on_toll_checkbox_active(self, checkbox, value):
        # Habilita ou desabilita a entrada do valor do pedágio
        self.toll_value.disabled = not value

    def calculate_fare(self, instance):
        # Aqui você pega os endereços do usuário
        start_address = self.start_address.text
        destination_address = self.destination_address.text
        chave_api = "SuaChaveDaAPI"

        # Chama a função para calcular a distância e duração
        resultado = calcular_distancia_duracao(start_address, destination_address, chave_api)

        if resultado:
            distancia, duracao = resultado
            # Aqui você pode adicionar a lógica para calcular o custo
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
