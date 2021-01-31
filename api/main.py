# importacion de libreria modulos
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from flask import render_template
from facebook import seleniumFacebook
import os 
import json
import codecs

app = Flask(__name__)
domains_allowed = ['http://ec2-54-84-79-47.compute-1.amazonaws.com']
cors = CORS(app, resources={r"/*": {"origins": domains_allowed}}) # 

# BASE = '/var/www/html/jd/'
BASE = 'api/'

'''
# RUTAS DE TEMPLATES
'''
@app.route('/')
def home():
    return redirect('tfe-idarevalos-train', code=301)

@app.route('/tfe-idarevalos')
def tfe_Home():
    return render_template('tfe/index.html')

@app.route('/tfe-idarevalos-train')
def tfe_Train():
    return render_template('tfe/try.html')

'''
# METODOS WEB DE EXTRACCION DE INFORMACION Y VALIDACION CON MODELO
'''
@app.route('/getDataProfile/<facebook_path>', methods=['GET'])
def getDataProfile(facebook_path):
    face = seleniumFacebook()
    
    # Extraccion de caracteristicas
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

# Lectura por filas de los perfiles almacenados en local
# Para la extraccion de caracteristicas
def readProfilesProcessRow(row_param = 0):
    
    new_row = {}

    ## Asignacion de Row con request cuando no se usa en funcion
    if row_param != 0:
        row = row_param
    else:
        row =  request.json
    
    # ## Numero de amigos   
    new_row['number_friends'] = row['number_friends']

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
        new_row['joined_in'] = cleanData('joined', row['joined_in'])
        new_row['joined_in_since'] = (2021 - cleanData('joined', row['joined_in']))

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

    ## RETORNO
    return new_row

def valideIAModelFacebook(data):
    
    ## Import Module
    import pickle

    array_to_prediction = []
    # return array_to_prediction
    cols = ['number_friends', 'followers','flag_study_actually','joined_in_since','live']

    for c in cols:
        array_to_prediction.append(data[c])
        
    ## ultimo append de prediccion
    array_to_prediction.append(0)

    ## CLASES DEFINIDAS
    group = ['Válido','No Válido']
    
    # pkl_filename = BASE+'00_model_kmeans_supervise.pkl'
    pkl_filename = BASE+'00_model_kmeans_supervise.pkl'
    # Load from file
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    
    Ypredict = pickle_model.predict([array_to_prediction])
    return group[Ypredict[0]]

'''
# METODOS INTERNOS DE EXTRACCION DE INFORMACION
'''
## Extraer informacion de amigos
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

## Lectura de perfiles almacenados en local
@app.route('/readProfiles')
def readProfiles():
    files = os.listdir('data/info-profiles/')
    content = []
    
    ## recorrer todos los archivos
    for file in files: # 90:200
        c_file = codecs.open('data/info-profiles/'+file,'r',"utf-8")
        txt_file = c_file.read().replace("'",'"')
        # print(file)
        content.append(readProfilesProcessRow(json.loads(txt_file)))

    return jsonify({
        "status":"success",
        "data": content,
        "count_files": len(files),
        "saved" : saveResult(str(content).replace("'",''),'final_data','00_json_result_scraping.json')
    })

'''
# METODOS AUXILIARES
'''
def saveResult(txt, folder, name_file):
        file = codecs.open('data/'+folder+'/'+name_file+'.txt','w',"utf-8")
        file.write(str(txt))
        file.close()
        return True

def cleanData(clean_to, txt_to_clean):
    final_txt = ''

    if clean_to == 'friends':
        if 'Daniel' in txt_to_clean:
            final_txt = txt_to_clean.replace('Daniel','')
        else:
            final_txt = txt_to_clean
        
        final_txt = final_txt.split(' ')
                    
        ## Recorre elementos con espacios
        all_empty = True

        for f_tx in final_txt:
            if f_tx != '':
                final_txt = f_tx
                all_empty = False

        ## Si esta vacio y no tiene amigos
        if all_empty:
            final_txt = '0'
    
        ## Comprobar si es un numero
        if final_txt.isnumeric():
            final_txt = int(final_txt)
        else:
            final_txt = 0

    if clean_to == 'joined':
        final_txt = txt_to_clean.split(' ')

        if len(final_txt) == 6:

            if final_txt[5].isnumeric():
                final_txt = int(final_txt[5])
            else:
                final_txt = 0
    
            
    return final_txt


# Inicializarlo
if __name__ == '__main__':
    app.run(debug=True, port=8080)