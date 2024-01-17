from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Bem-vindo ao TaxiApp!'))

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

    def on_checkbox_active(self, checkbox, value):
        self.start_address.disabled = value

    def on_toll_checkbox_active(self, checkbox, value):
        self.toll_value.disabled = not value

    def calculate_fare(self, instance):
        # Implemente a lógica para calcular a tarifa aqui
        print('Calculando tarifa...')

class TaxiApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CalculateScreen(name='calculate'))
        return sm

if __name__ == '__main__':
    TaxiApp().run()

