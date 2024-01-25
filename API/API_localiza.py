# // function getLocation() {
# //     if (navigator.geolocation) {
# //         navigator.geolocation.getCurrentPosition(showPosition, showError);
# //     } else { 
# //         console.log("Geolocalização não é suportada neste navegador.");
# //     }
# // }

# // function showPosition(position) {
# //     console.log("Latitude: " + position.coords.latitude + 
# //     "\nLongitude: " + position.coords.longitude);
# // }

# // function showError(error) {
# //     switch(error.code) {
# //         case error.PERMISSION_DENIED:
# //             console.log("Usuário negou a solicitação de geolocalização.");
# //             break;
# //         case error.POSITION_UNAVAILABLE:
# //             console.log("Informação de localização indisponível.");
# //             break;
# //         case error.TIMEOUT:
# //             console.log("A solicitação para obter a localização do usuário expirou.");
# //             break;
# //         case error.UNKNOWN_ERROR:
# //             console.log("Ocorreu um erro desconhecido.");
# //             break;
# //     }
# // }

# // getLocation();




from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/get_location', methods=['GET'])
def get_location():
    send_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCaUCyLGkWvCRKdlG8ITwK4WMRMVxtA9GQ'
    response = requests.post(send_url, json={})

    if response.status_code == 200:
        location_data = response.json()
        return jsonify(location_data)
    else:
        return jsonify({"error": "Não foi possível obter a localização", "status_code": response.status_code})

if __name__ == '__main__':
    app.run(debug=True)

