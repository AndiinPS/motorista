                                                          APS App

                                                         Descrição

O APS App é um aplicativo desenvolvido em Python utilizando a biblioteca Kivy. O aplicativo permite que os usuários se registrem, façam login e utilizem uma interface para calcular tarifas de táxi com base em endereços de embarque e destino. Ele também suporta a visualização de rotas no Google Maps e a obtenção de localização atual.

                                                      Funcionalidades

Registro e Login de Usuário: Permite que os usuários se registrem com nome, e-mail, data de nascimento e senha. Após o registro, um e-mail de confirmação é enviado ao usuário.
Login com Conta Google: Suporte para login com conta Google.
Calculadora de Tarifa: Calcula a tarifa estimada com base na distância entre o endereço de embarque e o destino, o valor do quilômetro e o valor do pedágio.
Autocompletar Endereços: Utiliza a API do Google Places para autocompletar endereços de embarque e destino.
Localização Atual: Permite obter a localização atual do usuário e preencher automaticamente o endereço de embarque.
Visualização de Rotas: Abre o Google Maps com a rota entre o endereço de embarque e o destino.

                                                        Requisitos

Python 3.x
Kivy
Requests
Google API (para mapas e geolocalização)

                                                        Instalação

Clone o repositório:

bash Copiar código git clone https://github.com/seu_usuario/aps_app.git

Navegue até o diretório do projeto:

bash Copiar código cd aps_app

Instale as dependências:

bash Copiar código pip install kivy requests google-api-python-client
Substitua as chaves da API do Google no código pelos seus valores.

                                                          Uso

Execute o aplicativo:

bash Copiar código python main.py
O aplicativo será iniciado e você verá a tela inicial com opções para login e registro.
