import time
import random
import string
from selenium import webdriver
from selenium.webdriver import ActionChains
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
    _driver = webdriver.Chrome(executable_path='C:\Python\chromedriver.exe')
    # executable_path='C:\Python\chromedriver.exe', options=options
    return _driver


def clearInput(*args):
    for x in args:
        x.clear()


def printCurrentAction(string):
    print(string + "...     ", end='')


def printActionResult(ok=True):
    if not ok:
        print("FAILURE\n\n")
    else:
        print("OK\n\n")


def sleepAndQuit(seconds):
    global driver
    time.sleep(seconds)
    print("!EXIT!")
    driver.quit()


def waitRandomTime(start=0.5, end=3.0):
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
    # name_url = "https://www.name-generator.org.uk/quick/"

    # opening second tab
    driver.execute_script('window.open("https://www.name-generator.org.uk/quick/");')
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

        _full_name = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[3]/div/div/form/div[1]'))).text

        time.sleep(1)

        # driver.close()
        # driver.switch_to.window((driver.window_handles[0]))
        return _full_name
    else:
        print("There is only 1 tab opened!")
        driver.quit()


def getMail():
    global driver
    mail_url = 'https://owlymail.com/'

    # opening second tab
    driver.get(mail_url)
    driver.switch_to.window(driver.window_handles[-1])

    #inside the second tab
    reset_button = WebDriverWait(driver, 8).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/div/div[1]/div[2]/form[2]/input[2]')))
    reset_button.click()

    _mail = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, 'current-id'))).get_attribute('value')
    time.sleep(1)

    #driver.close()

    # switch to instagram tab
    driver.switch_to.window((driver.window_handles[0]))

    return _mail


def saveCredentialsToFile(_credentials):
    file_name = 'credentials.txt'
    file = open(file_name, "a+")
    # print('file path: ', str(os.getcwd()) + '\\' + file_name)
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
        waitRandomTime(1, 3)
        # ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[7]/div/button')).click().perform()
        password_input.send_keys(Keys.RETURN)
        waitRandomTime()

    except Exception as ex:
        print(ex)
        driver.quit()


def chooseRandomValueFromPicklist(options_list, is_year_picklist=False):
    global driver

    random.seed()

    # making sure the age is >= 18
    if is_year_picklist:
        del options_list[0:18]

    picked_option = random.choice(options_list)
    print("\npicked option value: ", picked_option.text)
    picked_option.click()


def fillBirthdayForm():
    global driver

    if driver.current_url == 'https://www.instagram.com/accounts/emailsignup/':
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[3]/select'))
        )

        year_options = driver.find_elements_by_xpath(
            '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[3]/select/option')
        chooseRandomValueFromPicklist(year_options, is_year_picklist=True)
        waitRandomTime()

        month_options = driver.find_elements_by_xpath(
            '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[1]/select/option')
        chooseRandomValueFromPicklist(month_options)
        waitRandomTime()

        month_day_options = driver.find_elements_by_xpath(
            '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[2]/select/option')
        chooseRandomValueFromPicklist(month_day_options)
        waitRandomTime()

        ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/div[6]/button')).click().perform()



printCurrentAction('Starting the browser')
driver = getDriver()
printActionResult()

print('Browser session id: ', driver.session_id)
start_url = "https://www.instagram.com/accounts/emailsignup/"

print("Start page URL: " + start_url)
driver.get(start_url)
printActionResult()


printCurrentAction("Creating User credentials")
full_name = getRandomUsername()
user_name = generateUsername(full_name)
password = password_generator()
mail = getMail()
printActionResult()

# debug - instead of getMail
# driver.switch_to.window(driver.window_handles[0])

printCurrentAction("Filling registration form")
fillRegistration(mail, full_name, user_name, password)
printActionResult()

credentials = {
    "mail": mail,
    "full_name": full_name,
    "user_name": user_name,
    "password": password
}
print('User credentials: ', credentials)


printCurrentAction("Saving User credentials to file")
saveCredentialsToFile(credentials)
printActionResult()

printCurrentAction("Filling birthday form")
fillBirthdayForm()
printActionResult()

# sleepAndQuit(7)
