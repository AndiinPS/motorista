# // function calculateDistance() {
# //     var origin = new google.maps.LatLng(lat1, lon1); // Substitua por sua localização atual
# //     var destination = 'Endereço de Destino'; // Substitua pelo endereço de destino

# //     var service = new google.maps.DistanceMatrixService();
# //     service.getDistanceMatrix(
# //         {
# //             origins: [origin],
# //             destinations: [destination],
# //             travelMode: 'DRIVING',
# //         }, callback);
# // }

# // function callback(response, status) {
# //     if (status == 'OK') {
# //         var origins = response.originAddresses;
# //         var destinations = response.destinationAddresses;

# //         for (var i = 0; i < origins.length; i++) {
# //             var results = response.rows[i].elements;
# //             for (var j = 0; j < results.length; j++) {
# //                 var element = results[j];
# //                 var distance = element.distance.text;
# //                 var duration = element.duration.text;
# //                 var from = origins[i];
# //                 var to = destinations[j];
# //                 console.log(`Distância de ${from} até ${to}: ${distance}, tempo aproximado: ${duration}`);
# //             }
# //         }
# //     }
# // }



from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/calculate_distance', methods=['GET'])
def calculate_distance():
    lat1 = request.args.get('lat1')
    lon1 = request.args.get('lon1')
    destination_address = request.args.get('destination')

    api_key = 'AIzaSyCaUCyLGkWvCRKdlG8ITwK4WMRMVxtA9GQ'  # Substitua pela sua chave de API do Google Maps
    origin = f"{lat1},{lon1}"
    destination = destination_address

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        'origins': origin,
        'destinations': destination,
        'mode': 'driving',
        'key': api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        result = []
        for i in range(len(data['origin_addresses'])):
            origins = data['origin_addresses'][i]
            for j in range(len(data['destination_addresses'])):
                destinations = data['destination_addresses'][j]
                element = data['rows'][i]['elements'][j]
                distance = element['distance']['text']
                duration = element['duration']['text']
                result.append({
                    "origem": origins,
                    "destino": destinations,
                    "distância": distance,
                    "duração": duration
                })
        return jsonify(result)
    else:
        return jsonify({"error": "Erro ao calcular a distância", "status_code": response.status_code})

if __name__ == '__main__':
    app.run(debug=True)

