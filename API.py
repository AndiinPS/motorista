from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)



# Endpoint para verificar login
@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    username = dados.get('username')
    password = dados.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"message": "Nome de usuário ou senha incorretos."}), 401

# Endpoint para calcular a tarifa do táxi
@app.route('/calculate_fare', methods=['POST'])
def calculate_fare():
    dados = request.get_json()
    try:
        distance_to_start = 0 if dados['current_location'] else float(dados['start_address'])
        distance_to_destination = float(dados['distance'])
        total_distance = distance_to_start + distance_to_destination
        value_per_km = float(dados['value_per_km'])
        fare = total_distance * value_per_km

        if dados.get('toll_checkbox'):
            fare += float(dados['toll_value'])

        return jsonify({"fare": f'R${fare:.2f}'})
    except ValueError:
        return jsonify({"message": "Por favor, insira valores válidos."}), 400

if __name__ == '__main__':
    app.run(port=8080, host='localhost', debug=True)
