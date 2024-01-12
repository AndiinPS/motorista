from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.widget import Widget

class TaxiApp(GridLayout):

    def __init__(self, **kwargs):
        super(TaxiApp, self).__init__(**kwargs)
        self.cols = 2

        # Checkbox para local atual
        self.add_widget(Label(text='Já está no local de embarque?'))
        self.current_location_checkbox = CheckBox(active=True)
        self.current_location_checkbox.bind(active=self.on_checkbox_active)
        self.add_widget(self.current_location_checkbox)

        # Endereço de embarque
        self.add_widget(Label(text='Endereço de Embarque'))
        self.start_address = TextInput(multiline=False)
        self.start_address.disabled = True  # Desabilitado por padrão
        self.add_widget(self.start_address)

        # Endereço de destino
        self.add_widget(Label(text='Endereço de Destino'))
        self.destination_address = TextInput(multiline=False)
        self.add_widget(self.destination_address)

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
        if value:
            self.start_address.text = ''
            self.start_address.disabled = True
        else:
            self.start_address.disabled = False

    def calculate_fare(self, instance):
        # Aqui você fará o cálculo de fato, incluindo a lógica de API de mapas e pedágios
        self.result.text = 'Valor calculado da corrida aqui'

class MyApp(App):

    def build(self):
        return TaxiApp()

if __name__ == '__main__':
    MyApp().run()
