# importacion de libreria modulos
from flask import Flask, jsonify
from facebook import seleniumFacebook
import os 
import json
import codecs

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
@app.route('/getdata/<facebook_path>/<limit>', methods=['GET'])
def getData(facebook_path, limit):

    face = seleniumFacebook()
    data_facebook = face.start(facebook_path, limit)

    result = jsonify(
        {
            "status":"OK",
            "facebook_path":facebook_path,
            "facebook_result": data_facebook
        }
    )

    return result

# Peticion a servicio
@app.route('/getDataProfile/<facebook_path>', methods=['GET'])
def getDataProfile(facebook_path):
    face = seleniumFacebook()
    data_facebook = face.getDataProfile(facebook_path)

    result = jsonify(
        {
            "status":"OK",
            "facebook_path":facebook_path,
            "facebook_result": data_facebook
        }
    )

    return result

# recorrer todas los perfiles obtenidos
@app.route('/readProfiles')
def readProfiles():
    files = os.listdir('data/search-profiles/')
    content = ''

    for file in files:
        c_file = codecs.open('data/search-profiles/'+file,'r',"utf-8")
        content = c_file.read()

    return content


# # Leer perfiles, para convertirlos a un csv o json consolidado
# @app.route('/readProfiles')

# Inicializarlo
if __name__ == '__main__':
    app.run(debug=True, port=8080)
