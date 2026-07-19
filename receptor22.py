from flask import Flask, request
import webbrowser

app = Flask(__name__)

# Asegúrate de que la ruta sea exactamente '/orden'
@app.route('/orden', methods=['POST', 'GET'])
def recibir_orden():
    # El script del VPS envía un JSON con {'comando': 'Abre youtube.com'}
    data = request.json
    print(f"Datos recibidos: {data}")
    
    #ewjnfe
    
    if data and 'comando' in data:
        comando = data['comando'].lower()
        if "youtube" in comando:
            webbrowser.open("https://www.youtube.com")
            return {"status": "success", "message": "YouTube abierto"}, 200
            
    return {"status": "error", "message": "Ruta alcanzada pero comando no reconocido"}, 404

if __name__ == '__main__':
    # Puerto 7777 porque es el que configuramos en el túnel SSH
    app.run(host='0.0.0.0', port=7777)