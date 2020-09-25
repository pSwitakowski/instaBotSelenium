import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# for firefox compatibility
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def getDriver():
    # options = webdriver.FirefoxOptions()
    binary = FirefoxBinary('C:\\Users\\piotr.switakowski\\AppData\Local\\Mozilla Firefox\\firefox.exe')
    # options.add_argument("accept-language=en-US")  # self-explanatory
    # options.add_argument(
    # "--disable-blink-features=AutomationControlled")  # disables "automated" pop-up, also helps not getting detected (or not), doesnt work, probably bad name
    _driver = webdriver.Firefox(executable_path='C:\Python\geckodriver.exe', firefox_binary=binary)
    # executable_path='C:\Python\chromedriver.exe', options=options
    return _driver

def clearInput(*args):
    for x in args:
        x.clear()


def waitRandomTime():
    random.seed()
    time.sleep(random.uniform(0.1, 3.0))


def log_in(_login, _password):
    try:
        username_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
        password_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password')))

        clearInput(username_input, password_input)

        username_input.send_keys(_login)
        waitRandomTime()
        password_input.send_keys(_password)
        waitRandomTime()
        password_input.send_keys(Keys.RETURN)


    except Exception as ex:
        print(ex)
        driver.quit()


# binary = FirefoxBinary('C:\\Users\\piotr.switakowski\\AppData\Local\\Mozilla Firefox\\firefox.exe')
# driver = webdriver.Firefox(firefox_binary=binary, executable_path='C:\Python\geckodriver.exe')
driver = getDriver()

start_url = "https://instagram.com"
driver.get(start_url)

login = "nalif271@wp.pl"
password = "owlcity1"

log_in(login, password)


