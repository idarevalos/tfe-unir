from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from secrets import ida_u, ida_p

# Step 1) Open Firefox 
navigator = webdriver.Firefox(executable_path=r'C:\xampp\htdocs\idarevalos\unir\tfe-unir\api\assets\webdriver\geckodriver.exe')
# navigator = webdriver.Chrome(executable_path=r'C:\xampp\htdocs\idarevalos\unir\tfe-unir\api\assets\webdriver\geckodriver.exe')
# Step 2) Navigate to Facebook
navigator.get("http://www.facebook.com")
# Step 3) Search & Enter the Email or Phone field & Enter Password
username = navigator.find_element_by_id("email")
password = navigator.find_element_by_id("pass")
submit   = navigator.find_element_by_id("u_0_b")
username.send_keys(ida_u)
password.send_keys(ida_p)
# Step 4) Click Login
submit.click()


navigator.get('https://www.facebook.com/idarevalo1/friends')
friends = navigator.get_screenshot_as_png()
print(friends)

# for f in friends:
#     txt = f.text
#     print(txt)    

