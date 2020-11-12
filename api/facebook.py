from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import codecs

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
        navigator = webdriver.Firefox(executable_path=r'C:\xampp\htdocs\idarevalos\unir\tfe-unir\api\assets\webdriver\geckodriver.exe')
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

            if k['link'].find('profile.php') > 0:
                navigator.get(k['link']+'&sk=about') # Informacion basica
            else:
                navigator.get(k['link']+'/about_overview') # Informacion basica

            time.sleep(1.5)

            profile_information = {}
            profile_information['me'] = self.decodePathFacebook(k['link'])
            profile_information['friend'] = facebook_path
            profile_information['estudy'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div'))
            profile_information['live'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[3]/div/div/div[2]/div'))
            profile_information['from'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div'))
            profile_information['marital_status'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[2]'))
            profile_information['phone'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[6]/div/div/div[2]/div[1]'))

            result_obj = {
                facebook_path: profile_information
            }

            self.saveResult(result_obj, 'info-profiles', self.decodePathFacebook(k['link']))
            time.sleep(0.5)
        
        time.sleep(1)
        return li

    def processElementHtml(self, ele):
        """
        Procesa el objeto entregado por selenium y retorna el .text
        """
        r = ''
        for i in ele:
            r = i.text
        
        return r

    def getDataProfile(self, facebook_path):

        
        navigator = webdriver.Firefox(executable_path=r'C:\xampp\htdocs\idarevalos\unir\tfe-unir\api\assets\webdriver\geckodriver.exe')
        navigator.get("http://www.facebook.com")
        
        username = navigator.find_element_by_id("email")
        password = navigator.find_element_by_id("pass")
        submit   = navigator.find_element_by_id("u_0_b")
        username.send_keys(self.u)
        password.send_keys(self.p)

        submit.click()

        time.sleep(1)
        
        navigator.get('https://www.facebook.com/'+facebook_path+'/about_overview') # Informacion basica
        
        profile_information = {}

        profile_information['estudy'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div'))
        profile_information['live'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[3]/div/div/div[2]/div'))
        profile_information['from'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div'))
        profile_information['marital_status'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[2]'))
        profile_information['phone'] = self.processElementHtml(navigator.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[6]/div/div/div[2]/div[1]'))


        return profile_information

    def decodePathFacebook(self, path___):
        r = ''
        if path___.find('profile.php?id=') > 0:
            p = path___.split('profile.php?id=')
            r = p[1]
        else:
            p = path___.split('https://www.facebook.com/')
            r = p[1]

        return r
