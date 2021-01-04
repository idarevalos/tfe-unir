# importacion de libreria modulos
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import render_template
from facebook import seleniumFacebook
import os 
import json
import codecs

import pickle
import numpy as np
import pandas as pd
import base64
import requests 

app = Flask(__name__)
domains_allowed = ['http://ec2-54-84-79-47.compute-1.amazonaws.com']
cors = CORS(app, resources={r"/*": {"origins": domains_allowed}}) # 



'''
/*
    PRACTICAS
*/
'''

@app.route('/practicas')
def practicasHome():
    return render_template('practicas/index.html')


# Peticion a servicio
@app.route('/processPreferences/<preferences>', methods=['GET'])
def processPreferences(preferences):
    
    J = base64.b64decode(preferences).decode("utf-8", "strict")
    X = pd.DataFrame(data=json.loads(J))
        
    result = jsonify(
        {
            "status":"OK",
            "data": valideIAModel(X),
            'related': getRelated(json.loads(J))
        }
    )

    return result

# Validacion de modelo
def valideIAModel(data):
    
    pkl_filename = '/var/www/html/jd/00_model_desition_tree.pkl'
    # pkl_filename = 'api/00_model_desition_tree.pkl'
    # Load from file
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    
    Ypredict = pickle_model.predict(data)
    return processResponcePredict(Ypredict[0])

# Procesar con prediccion
@app.route('/searchOtherInfo/<predict_data>', methods=['GET'])
def processResponcePredict(predict_data):
    URL = 'https://api.ciencuadras.com/api/realestate?realEstateCode='+predict_data
    r = requests.get(url = URL) 

    return r.json()


def getRelated(data):
    
    arr_result = {}
    arr_result['count'] = 0
    arr_result['result'] = []

    # f = codecs.open('api/PROCESS_DATA.txt', "r", "utf-8")
    f = codecs.open('/var/www/html/jd/PROCESS_DATA.txt', "r", "utf-8")
    data_json = json.loads(f.read())

    
    
    for e in data_json[0:100]:
        
        if e['precio_venta_original'] == data['precio_venta_original'][0]:
            if e not in arr_result['result']:
                arr_result['count'] = arr_result['count'] + 1
                arr_result['result'].append(e)
        
        if int(e['antiguedad']) == int(data['antiguedad'][0]):
            if e not in arr_result['result']:
                arr_result['count'] = arr_result['count'] + 1
                arr_result['result'].append(e)

        if int(e['valor_administracion']) == int(data['valor_administracion'][0]):
            if e not in arr_result['result']:
                arr_result['count'] = arr_result['count'] + 1
                arr_result['result'].append(e)

        if int(e['num_depositos']) == int(data['num_depositos'][0]):
            if e not in arr_result['result']:
                arr_result['count'] = arr_result['count'] + 1
                arr_result['result'].append(e)

        if int(e['zona_infantil']) == int(data['zona_infantil'][0]):
            if e not in arr_result['result']:
                arr_result['count'] = arr_result['count'] + 1
                arr_result['result'].append(e)

    return arr_result



'''
/*
TFE - PRACTICAS UNIR
*/
'''

@app.route('/tfe-idarevalos')
def tfe_Home():
    return render_template('tfe/index.html')

@app.route('/tfe-idarevalos-train')
def tfe_Train():
    return render_template('tfe/try.html')

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
    process_data = readProfilesProcessRow(data_facebook)
    prediction_data = valideIAModelFacebook(process_data)

    result = jsonify(
        {
            "status":"OK",
            "facebook_path":facebook_path,
            "facebook_result": data_facebook,
            "result_process_data": process_data,
            "result_prediction": prediction_data
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
        content.append(readProfilesProcessRow(json.loads(txt_file)))

    return jsonify({
        "status":"success",
        "data": content,
        "count_files": len(files),
        "saved" : saveResult(str(content).replace("'",''),'final_data','00_json_result_scraping.json')
    })
    
    # return jsonify(content)

## Procesar cada linea para extraer informacion de los perfiles
@app.route('/readProfilesProcessRow', methods=['POST'])
def readProfilesProcessRow(row_param = 0):

    new_row = {}
    ## Asignacion de Row con request cuando no se usa en funcion
    if row_param != 0:
        row = row_param
    else:
        row =  request.json
    

    ## Numero de amigos
    
    t = row['number_friends'].split(' ')      
    it = t[0]
    
    ## Validando cuando existe texto de nombre de perfil
    ## daniel
    if t[0] == 'Daniel':
        it = t[1]

    if it.isnumeric():
        new_row['number_friends'] = int(it)
    else:
        new_row['number_friends'] = 0
    
    ## Folowers
    if 'followers' in row:
        f = row['followers'].split(' ')
        f1 = f[0].replace('.','')
        new_row['followers'] = int(f1)
    else:
        new_row['followers'] = 0
    
    ## Job
    if 'job' in row:
        new_row['job'] = 1
    else:
        new_row['job'] = 0
    
    # joined in
    if 'joined_in' in row:
        tj = row['joined_in'].split(' ')
        new_row['joined_in'] = int(tj[5]) ## numero del anio
        new_row['joined_in_since'] = (2021 - row['joined_in'])
    else:
        new_row['joined_in'] = 0
        new_row['joined_in_since'] = 0

    ## Live
    if 'live' in row:
        new_row['live'] = 1
    else:
        new_row['live'] = 0

    ## Live
    if 'study_actually' in row:
        new_row['study_actually'] = 1
        new_row['flag_study_actually'] = 1
    else:
        new_row['study_actually'] = 0
        new_row['flag_study_actually'] = 0

    ## Remove rows
    new_row['name'] = 1
    new_row['me'] = 1
    new_row['friend'] = 1
    new_row['name_user_sub'] = 1
    new_row['study_finish'] = 1

    # new_row = str(new_row).replace("'",'"')

    ## RETORNO
    return new_row

# Validacion de modelo
def valideIAModelFacebook(data):

    array_to_prediction = []
    # return array_to_prediction
    cols = ['number_friends', 'followers','flag_study_actually','joined_in_since','live']

    for c in cols:
        array_to_prediction.append(data[c])
        
    ## ultimo append de prediccion
    array_to_prediction.append(0)

    ## CLASES DEFINIDAS
    group = ['Válido','No Válido']
    
    pkl_filename = '/var/www/html/jd/00_model_kmeans_supervise.pkl'
    # pkl_filename = 'api/00_model_kmeans_supervise.pkl'
    # Load from file
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    
    Ypredict = pickle_model.predict([array_to_prediction])
    return group[Ypredict[0]]


'''
/*
END TFE - PRACTICAS UNIR
*/
'''


def saveResult(txt, folder, name_file):
        file = codecs.open('data/'+folder+'/'+name_file,'w',"utf-8")
        file.write(str(txt))
        file.close()
        return True


# Inicializarlo
# if __name__ == '__main__':
#     app.run(debug=True, port=8080)