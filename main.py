from flask import Flask, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
domains_allowed = ['http://idarevalos.co']
cors = CORS(app, resources={r"/*": {"origins": domains_allowed}}) # 


@app.route('/queryProfile/<profile>')
def queryProfile(profile):
    p = base64.b64decode(profile).decode("utf-8", "strict")

    return jsonify(
        {
            "status":"OK",
            "description":'Se está procesando información para el perfil de: '+str(p)
        }
    )


# Inicializarlo
if __name__ == '__main__':
    # app.run(debug=False, port=443)
    app.run(debug=True, port=8080)

