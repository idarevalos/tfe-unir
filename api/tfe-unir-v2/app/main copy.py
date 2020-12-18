# importacion de libreria modulos
from flask import Flask, jsonify
from flask_cors import CORS
from app import scraper

app = Flask(__name__)

domains_allowed = ['http://idarevalos.co','https://idarevalos-tfe-unir.web.app']
cors = CORS(app, resources={r"/*": {"origins": domains_allowed}}) # 


# Peticion a servicio
@app.route('/getDataProfile/<facebook_path>', methods=['GET'])
def getDataProfile(facebook_path):
    
    t = scraper()
    # t = ':)'

    result = jsonify(
        {
            "status":"OK",
            "data":t
        }
    )

    return result

@app.route("/")
def home():
    result = jsonify(
        {
            "status":"OK",
            "data":":)"
        }
    )
    return result
# Inicializarlo
# if __name__ == '__main__':
  #  app.run(debug=True, port=8080)
    # app.run(debug=False, port=443)
