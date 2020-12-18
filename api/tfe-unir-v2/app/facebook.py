from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import codecs
from bs4 import BeautifulSoup
import json

class seleniumFacebook():

    def __init__(self, **kwargs):
        self.u = "ivandaniel.arevalo884@comunidadunir.net"
        self.p = "TFFMKMGZEN"

    def saveResult(self, txt, folder, name_file):
        file = codecs.open('data/'+folder+'/'+name_file,'w',"utf-8")
        file.write(str(txt))
        file.close()
        return True
    
    def start(self, facebook_path, limit):
        # Seleccionar navegador
        navigator = webdriver.Firefox(executable_path=r'https://idarevalos.s3.amazonaws.com/tfe-unir/webdrivers/geckodriver.exe') #C:\xampp\htdocs\idarevalos\unir\tfe-unir\api\assets\webdriver\geckodriver.exe
        navigator.get("http://www.facebook.com")
        # Step 3) Search & Enter the Email or Phone field & Enter Password
        username = navigator.find_element_by_id("email")
        password = navigator.find_element_by_id("pass")
        submit   = navigator.find_element_by_id("u_0_b")
        username.send_keys(self.u)
        password.send_keys(self.p)
        # Step 4) Click Login
        submit.click()
        # time 1 seg
        time.sleep(1)

        navigator.get('https://www.facebook.com/'+facebook_path+'/friends')
        limit_scroll = 15
        for t in range(limit_scroll):
            time.sleep(0.5)
            navigator.execute_script('window.scroll(0, '+str(1000*t)+')')    

        time.sleep(4)
        li = []
        limit_friends = int(limit) 

        # insre links
        for lf in range(limit_friends):
            path__ = '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[3]/div['+str(lf)+']/div[2]/div[1]/a' # a/span
            
            if lf > 0:
                friends = navigator.find_elements_by_xpath(path__)

                # Recorrer los elementos encontrados
                for f in friends:
                    li.append(
                        {
                            "link": f.get_attribute('href')
                        }
                    )
        
        ## Recorrer los links creados y asignar name
        for r in range(len(li)):
            item = r+1 # Corresponde a la asignacion correcta de link + name

            path__ = '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[3]/div['+str(item)+']/div[2]/div[1]/a/span' # a/span
            
            fx = navigator.find_elements_by_xpath(path__)
            # Recorrer los elementos encontrados
            for f in fx:
                li[r]['name'] = f.text
                
        
        # Guardar amigos general
        self.saveResult(li, 'search-profiles', facebook_path)
        li.append({"name":"","link":"https://www.facebook.com/"+facebook_path})

        for k in li:

            # if k['link'].find('profile.php') > 0:
            #     navigator.get(k['link']+'&sk=about') # Informacion basica
            # else:
            #     navigator.get(k['link']+'/about_overview') # Informacion basica
            
            navigator.get(k['link']) # Informacion basica
            time.sleep(5)

            profile_information = {}
            profile_information['me'] = self.decodePathFacebook(k['link'])
            profile_information['friend'] = facebook_path


            ### START
            source_code=navigator.page_source
            soup = BeautifulSoup(source_code, 'html.parser')

            name_user = soup.select('h1.gmql0nx0') 
            profile_information['name'] = self.processElementHtml(name_user)

            name_user_sub = soup.select('div.obtkqiv7:nth-child(2) > div:nth-child(1) > span:nth-child(1)')
            profile_information['name_user_sub'] = self.processElementHtml(name_user_sub)

            number_friends = soup.select('span.d2edcug0:nth-child(2)')
            profile_information['number_friends'] = self.processElementHtml(number_friends)
    

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
                }            
            ]

            for at in attrs:
                if at['type'] == 'txt':
                    for item in soup.select(at['selector']):
                        ## recorriendo todos los elementos
                        it = str(item.get_text())
                        if at['target'] in it:
                            profile_information[at['name_target']] = it.replace('"','').replace('/','')
                else:
                    item = soup.select(at['selector'])
                    profile_information[at['name_target']] = self.processElementHtml(item)

            
            ## procesando los datos generados
            ## obtener banderas de los datos que fueron obtenidos
            save_data = False
            if 'study_finish' in profile_information.keys():
                save_data = True
                if 'Estudia en' in profile_information['study_finish']:
                    profile_information['flag_study_actually'] = 1
                else:
                    profile_information['flag_study_actually'] = 0
            else:
                profile_information['flag_study_actually'] = 0

            if 'study_actually' in profile_information.keys():
                profile_information['flag_study_actually'] = 1
                save_data = True
            elif'joined_in' in profile_information.keys():
                save_data = True
            elif'study_finish' in profile_information.keys():
                profile_information['flag_study_actually'] = 0
                save_data = True
                

            ## END 
            
            
            if save_data:
                self.saveResult(profile_information, 'info-profiles', self.decodePathFacebook(k['link']))
            time.sleep(0.5)
        
        time.sleep(1)
        return li

    def processElementHtml(self, ele):
        """
        Procesa el elemento exportado de BS4, y retorna un texto concatenado
        """
        txt_r = ''
        for element in ele:
            txt_r += str(element.get_text().replace('"','').replace("'",'').replace('/',''))+' '
        
        return txt_r

    def getDataProfile(self, facebook_path):

        
        CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument('--no-sandbox')
        navigator = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                chrome_options=chrome_options
                                )
        
        
        ## Autenticacion en Facebook
        navigator.get("http://www.facebook.com")
        time.sleep(5) # time 1 seg

        username = navigator.find_element_by_id("email")
        password = navigator.find_element_by_id("pass")
        submit   = navigator.find_element_by_id("u_0_b")
        username.send_keys(self.u)
        password.send_keys(self.p)
        submit.click()
        
        time.sleep(0.5) # time 1 seg
        profile_information = {} ## define el objeto donde se almacenan los datos
        
        # navegar en home del perfil
        navigator.get('https://www.facebook.com/'+facebook_path) # 

        time.sleep(3) # time 1 seg

        ### START
        source_code=navigator.page_source
        soup = BeautifulSoup(source_code, 'html.parser')

        name_user = soup.select('h1.gmql0nx0') 
        profile_information['name'] = self.processElementHtml(name_user)

        name_user_sub = soup.select('div.obtkqiv7:nth-child(2) > div:nth-child(1) > span:nth-child(1)')
        profile_information['name_user_sub'] = self.processElementHtml(name_user_sub)

        number_friends = soup.select('span.d2edcug0:nth-child(2)')
        profile_information['number_friends'] = self.processElementHtml(number_friends)
   

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
            }            
        ]
        for at in attrs:
            if at['type'] == 'txt':
                for item in soup.select(at['selector']):
                    ## recorriendo todos los elementos
                    it = str(item.get_text())
                    if at['target'] in it:
                        profile_information[at['name_target']] = it
            else:
                item = soup.select(at['selector'])
                profile_information[at['name_target']] = self.processElementHtml(item)

        
        ## procesando los datos generados
        ## obtener banderas de los datos que fueron obtenidos
        # if 'Estudia en' in profile_information['study_finish']:
        #     profile_information['flag_study_actually'] = 1
        # else:
        #     profile_information['flag_study_actually'] = 0
            

        ## END 

        return profile_information
        navigator.close()

    def decodePathFacebook(self, path___):
        r = ''
        if path___.find('profile.php?id=') > 0:
            p = path___.split('profile.php?id=')
            r = p[1]
        else:
            p = path___.split('https://www.facebook.com/')
            r = p[1]

        return r
