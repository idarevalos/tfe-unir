# importacion de libreria modulos
from flask import Flask, jsonify
from data import products
import urllib.request


app = Flask(__name__)

# Creacion de Rutas
@app.route('/home')
def start():
    return jsonify(
        {
            "status":"OK",
            "data":products
        }
    )

# Peticion a servicio
@app.route('/getdata')
def getData():
    response = urllib.request.urlopen('http://localhost/home')
    html = response.read()
    return html

# Inicializarlo
if __name__ == '__main__':
    app.run(debug=True, port=80)
