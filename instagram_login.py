from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# for firefox compatibility
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.support.wait import WebDriverWait


def clearLoginInput(login_input, password_input):
    login_input.clear()
    password_input.clear()


def log_in(_login, _password):
    try:
        username_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
        password_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password')))

        clearLoginInput(username_input, password_input)

        username_input.send_keys(login)
        driver.implicitly_wait(1)
        password_input.send_keys(password)
        driver.implicitly_wait(2)
        password_input.send_keys(Keys.RETURN)
    except Exception as ex:
        print(ex)
        driver.quit()


binary = FirefoxBinary('C:\\Users\\piotr.switakowski\\AppData\Local\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path='C:\Python\geckodriver.exe')
# driver = webdriver.Chrome('C:\Python\chromedriver.exe')
driver.get("https://instagram.com")

login = "nalif271@wp.pl"
password = "owlcity1"

log_in(login, password)

# driver.quit()

