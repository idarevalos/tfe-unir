# importacion de libreria modulos
from flask import Flask, jsonify
from flask_cors import CORS
from facebook import seleniumFacebook
import os 
import json
import codecs

app = Flask(__name__)
domains_allowed = ['http://idarevalos.co','https://idarevalos-tfe-unir.web.app']
cors = CORS(app, resources={r"/*": {"origins": domains_allowed}}) # 


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
    files = os.listdir('data/info-profiles/')
    content = []
    
    ## recorrer todos los archivos
    for file in files:
        c_file = codecs.open('data/info-profiles/'+file,'r',"utf-8")
        txt_file = c_file.read().replace("'",'"')
        content.append(json.loads(txt_file))       
        
    # return jsonify({
    #     "status":"success",
    #     "data": content,
    #     "count_files": len(files)
    # })
    return jsonify(content)


# Inicializarlo
# if __name__ == '__main__':
#     app.run(debug=True, port=8080)
