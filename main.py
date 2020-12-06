from flask import Flask, jsonify
import boto3
from credentials_aws import key, sec_key, region_name
from botocore.exceptions import ClientError
import json

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

@app.route('/welcome')
def welcome():
    return jsonify(
        {
            "status":"OK",
            "data":'success welcome update unir'
        }
    )


# Inicializarlo
if __name__ == '__main__':
    # app.run(debug=False, port=443)
    app.run(debug=True, port=8080)

