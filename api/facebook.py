from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

import time
import codecs
from bs4 import BeautifulSoup
import json

# BASE = '/var/www/html/jd/'
BASE = ''

class seleniumFacebook():

    def __init__(self, **kwargs):
        self.u = "ivandaniel.arevalo884@comunidadunir.net"
        self.p = "TFFMKMGZEN"     

        # self.CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
        self.CHROMEDRIVER_PATH = 'api/webdriver/geckodriver.exe'
        self.WINDOW_SIZE = "1920,1080"

        ## Google Chrome options
        # self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_argument("--window-size=%s" % self.WINDOW_SIZE)
        # self.chrome_options.add_argument('--no-sandbox')

        # self.navigator = webdriver.Chrome(executable_path = self.CHROMEDRIVER_PATH, chrome_options = self.chrome_options)

        ## Firefox Options
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=%s" % self.WINDOW_SIZE)
        self.navigator = webdriver.Firefox(options=self.options, executable_path = self.CHROMEDRIVER_PATH)
                
    def decodePathFacebook(self, path___):
        r = ''
        if path___.find('profile.php?id=') > 0:
            p = path___.split('profile.php?id=')
            r = p[1]
        else:
            p = path___.split('https://www.facebook.com/')
            r = p[1]

        return r

    # Retorna informacion del perfil del usuario
    def getDataProfile(self, facebook_path, type = 'web'):

        ## Autenticacion en Facebook, cuando la peticion es de web
        if type == 'web':

            self.navigator.get("http://www.facebook.com")
            time.sleep(2) # time 1 seg

            username = self.navigator.find_element_by_id("email")
            password = self.navigator.find_element_by_id("pass")
            submit   = self.navigator.find_element_by_name("login")

            username.send_keys(self.u)
            password.send_keys(self.p)
            submit.click()
        
        time.sleep(0.5) # time 1 seg
        profile_information = {} ## define el objeto donde se almacenan los datos
        
        # navegar en home del perfil
        self.navigator.get('https://www.facebook.com/'+facebook_path) # 

        time.sleep(3) # time 1 seg

        ### START
        source_code= self.navigator.page_source
        soup = BeautifulSoup(source_code, 'html.parser')

        name_user = soup.select('h1.gmql0nx0') 
        profile_information['name'] = self.processElementHtml(name_user)

        name_user_sub = soup.select('div.obtkqiv7:nth-child(2) > div:nth-child(1) > span:nth-child(1)')
        profile_information['name_user_sub'] = self.processElementHtml(name_user_sub)

        number_friends = soup.select('span.e9vueds3:nth-child(2)')
        number_friends = self.processElementHtml(number_friends)
        profile_information['number_friends'] = self.cleanData('friends', number_friends)
   

        ## procesar informacion persolan
        attrs = [
            {
                'selector':'span',
                'target': 'Se unió en:',
                'type':'txt',
                'name_target': 'joined_in'
            },
            {
                'selector':'span',
                'target': 'Estudió en',
                'type':'txt',
                'name_target': 'study_finish'
            },
            {
                'selector':'span',
                'target': 'Estudia en',
                'type':'txt',
                'name_target': 'study_actually'
            },
            {
                'selector':'span',
                'target': 'Vive en',
                'type':'txt',
                'name_target': 'live'
            },
            {
                'selector':'span',
                'target': 'seguidores',
                'type':'txt',
                'name_target': 'followers'
            },
            {
                'selector':'div.lpgh02oy:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)',
                'target': 'job',
                'type':'selector',
                'name_target': 'job'
            },
            {
                'selector':'div.cwj9ozl2:nth-child(1) > a:nth-child(1) > div:nth-child(1) > svg:nth-child(1) > g:nth-child(2) > image:nth-child(1)',
                'target': 'profile_image',
                'type':'image',
                'name_target': 'profile_image'
            },
            {
                'selector':'div.oo9gr5id > div:nth-child(1) > svg:nth-child(1) > g:nth-child(2) > image:nth-child(1)',
                'target': 'profile_image',
                'type':'image',
                'name_target': 'profile_image'
            }            
        ]
        
        ## def image
        img = 'none'

        for at in attrs:
            
            if at['type'] == 'txt':
                for item in soup.select(at['selector']):
                    ## recorriendo todos los elementos
                    it = str(item.get_text())
                    if at['target'] in it:
                        profile_information[at['name_target']] = it

            elif at['type'] == 'selector':
                item = soup.select(at['selector'])
                profile_information[at['name_target']] = self.processElementHtml(item)

            elif at['type'] == 'image':

                item = soup.select(at['selector'])                
                for im in soup.select(at['selector']):
                    if img == 'none':
                        img = im.get_attribute_list('xlink:href')[0]                        
                    
                profile_information[at['name_target']] = str(img)

        # Cierro el navegador solo si es de web,
        # si se corre proceso interno, no se cierra
        if type == 'web':
            self.navigator.close()

        ## Guarda el resultado, solo cuando el nuevo perfil tiene informacion de amigos
        if self.cleanData('friends', number_friends) > 0 or type == 'web':
            self.saveResult(profile_information, 'info-profiles', facebook_path)

        return profile_information
        
    def processElementHtml(self, ele):
        """
        Procesa el elemento exportado de BS4, y retorna un texto concatenado
        """
        txt_r = ''  
        for element in ele:
            txt_r += str(element.get_text().replace('"','').replace("'",'').replace('/',''))+' '
        
        return txt_r
    
    def saveResult(self, txt, folder, name_file):
        file = codecs.open(BASE+'data/'+folder+'/'+name_file+'.txt','w',"utf-8")
        file.write(str(txt))
        file.close()
        return True

    def cleanData(self, clean_to, txt_to_clean):
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

    ## Consulta perfiles de amigos de un perfil de facebook
    def start(self, facebook_path, limit):
        
        self.navigator.get("http://www.facebook.com")
        time.sleep(1)

        username = self.navigator.find_element_by_id("email")
        password = self.navigator.find_element_by_id("pass")
        submit   = self.navigator.find_element_by_name("login")
        
        username.send_keys(self.u)
        password.send_keys(self.p)

        # Step 4) Click Login
        submit.click()
        # time 1 seg
        time.sleep(1)

        self.navigator.get('https://www.facebook.com/'+facebook_path+'/friends')
        limit_scroll = 20
        for t in range(limit_scroll):
            time.sleep(0.5)
            self.navigator.execute_script('window.scroll(0, '+str(1000*t)+')')    

        
        ## extraccion de informacion con BS4
        source_code= self.navigator.page_source
        soup = BeautifulSoup(source_code, 'html.parser')

        time.sleep(6)
        li = []
        limit_friends = int(limit) 


        # insre links
        for lf in range(limit_friends):
            
            item_search = lf + 1
            item_find = soup.select('div.bp9cbjyn:nth-child('+str(item_search)+') > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
            
            # Solo si existe elemento por consultar
            if len(item_find) > 0:           
                li.append(
                    {
                        "link": item_find[0]['href']
                    }
                )
                
        li.append({"link":"https://www.facebook.com/"+facebook_path})

        ## Guardar link de perfil de amigos
        self.saveResult(li, 'search-profiles', facebook_path)
        
        
        # Extraer la informacion de cada perfil consultado
        for k in li:
            link_facebook = self.decodePathFacebook(k['link'])
            self.getDataProfile(link_facebook, 'start_method')

        ## Terminar proceso, cerrar navegador y responder
        self.navigator.close()
        time.sleep(0.5)
        return li
        