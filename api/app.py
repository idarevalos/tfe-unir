# importacion de libreria modulos
from flask import Flask, jsonify

app = Flask(__name__)

# Ruta principal
@app.route('/home')
def home():
    return jsonify(
        {
            "status":"OK",
            "data":'empty'
        }
    )

# Peticion a servicio
@app.route('/getdata/<facebook_path>', methods=['GET'])
def getData(facebook_path):
    return jsonify(
        {
            "status":"OK",
            "facebook_path":facebook_path
        }
    )

# Inicializarlo
if __name__ == '__main__':
    app.run(debug=True, port=8080)
