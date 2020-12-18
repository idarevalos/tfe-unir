from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scraper():
        
    CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                            chrome_options=chrome_options
                            )

    # options = webdriver.ChromeOptions()
    # options.binary_location = "/usr/bin/google-chrome"
    # chrome_driver_binary = "/usr/local/bin/chromedriver"

    # driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

    driver.get("https://www.youtube.com/")
    return driver.title
    driver.close()