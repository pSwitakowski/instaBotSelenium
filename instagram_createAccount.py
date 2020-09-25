import time
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# for firefox compatibility
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")  # self-explanatory
    #options.add_argument(
    #     "--disable-blink-features=AutomationControlled")  # disables "automated" pop-up, also helps not getting detected (or not), doesnt work, probably bad name
    _driver = webdriver.Firefox(executable_path='C:\Python\geckodriver.exe')
    # executable_path='C:\Python\chromedriver.exe', options=options
    return _driver


def clearInput(*args):
    for x in args:
        x.clear()


def waitRandomTime(start=0.1, end=3.0):
    random.seed()
    time.sleep(random.uniform(start, end))


def id_generator(size=3, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def password_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generateUsername(_full_name):
    return _full_name.replace(" ", ".") + '.' + id_generator()


def getRandomUsername():
    global driver
    mail_url = 'https://temp-mail.org/pl/'

    # opening second tab
    driver.execute_script('window.open({});'.format(mail))
    if len(driver.window_handles) > 1:
        print("Switching to the second tab...")
        driver.switch_to.window(driver.window_handles[-1])

        _full_name = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/form/div[1]'))).text
        time.sleep(1)

        # driver.close()
        # driver.switch_to.window((driver.window_handles[0]))
        return _full_name
    else:
        print("There is only 1 tab opened!")
        driver.quit()


def getMail():
    global driver
    mail_url = 'https://temp-mail.org/pl/'

    # opening second tab
    driver.get(mail_url)
    print("Switching to the second tab...")
    driver.switch_to.window(driver.window_handles[-1])

    #inside the second tab
    WebDriverWait(driver, 8).until(
    EC.presence_of_element_located((By.ID, 'click-to-delete'))).click()

    _mail = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, 'mail'))).text
    print('MAIL: ' + _mail)
    time.sleep(1)

    #driver.close()
    #driver.switch_to.window((driver.window_handles[0]))
    return _mail


def saveCredentialsToFile(_credentials):
    file_name = 'credentials.txt'
    file = open(file_name, "a+")
    print('file path: ', str(os.getcwd()) + '\\' + file_name)
    file.write(str(_credentials))
    file.write('\n')
    file.close()


def fillRegistration(_mail, _full_name, _user_name, _password):
    try:
        mail_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'emailOrPhone')))
        full_name_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'fullName')))
        user_name_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
        password_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password')))

        clearInput(mail_input, full_name_input, user_name_input, password_input)

        mail_input.send_keys(_mail)
        waitRandomTime()

        full_name_input.send_keys(_full_name)
        waitRandomTime()

        user_name_input.send_keys(_user_name)
        waitRandomTime()

        password_input.send_keys(_password)
        waitRandomTime()

        # password_input.send_keys(Keys.RETURN)
    except Exception as ex:
        print(ex)
        driver.quit()


print('starting the browser...')
driver = getDriver()
print('browser session id: ', driver.session_id)
start_url = "https://www.instagram.com/accounts/emailsignup/"
print('opening page: ',start_url)
driver.get(start_url)


print('creating user credentials...')
full_name = getRandomUsername()
user_name = generateUsername(full_name)
password = password_generator()
mail = getMail()

print('filling the registration form...')
fillRegistration(mail, full_name, user_name, password)


credentials = {
    "mail": mail,
    "full_name": full_name,
    "user_name": user_name,
    "password": password
}
print('user credentials: ', credentials)

print('saving credentials to file...')
saveCredentialsToFile(credentials)

getMail()
# print(getMail())
