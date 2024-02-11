from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

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
    pass

class APSApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CalculateScreen(name='calculate'))  # Adiciona a tela "calculate" ao ScreenManager
        return sm

if __name__ == '__main__':
    APSApp().run()
