import time
import random
import string
import pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType


class RegistrationDriver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # PROXY = "147.135.7.122:3128"
        options.add_argument("accept-language=en-US")  # set english browser language
        options.add_argument("--start-maximized")  # set full screen browser
        # options.add_argument('--proxy-server=%s' % PROXY)  # set proxy
        options.add_argument("--disable-blink-features=AutomationControlled")  # disables "automated" pop-up, also helps not getting detected (or not), doesnt work hehe

        self.driver = webdriver.Chrome(executable_path='C:\Python\chromedriver.exe', options=options)

    def close_browser(self):
        time.sleep(2)
        print("!EXIT!")
        self.driver.quit()


    def generate_id(self, size=4):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def generate_password(self, size=10):
        return ''.join(random.choice(chars=string.ascii_letters + string.digits) for _ in range(size))

    def generate_username(self, _full_name):
        return _full_name.replace(" ", ".") + '.' + self.generate_id()

    def get_random_fullname(self):

        # name_url = "https://www.name-generator.org.uk/quick/"
        # opening second tab
        self.driver.execute_script('window.open("https://www.name-generator.org.uk/quick/");')
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(driver.window_handles[-1])

            _full_name = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[3]/div/div/form/div[1]'))).text

            time.sleep(1)

            return _full_name
        else:
            print("There is only 1 tab opened!")
            self.driver.quit()

    def get_random_mail(self):
        mail_url = 'https://temp-mail.org/pl/'

        # opening second tab
        self.driver.get(mail_url)
        self.driver.switch_to.window(driver.window_handles[-1])

        # inside the second tab
        reset_button = WebDriverWait(self.driver, 8).until(
            EC.presence_of_element_located((By.ID, 'click-to-delete')))
        reset_button.click()

        time.sleep(5)

        # _mail = WebDriverWait(driver, 10).until(
        #     EC.text_to_be_present_in_element_value('mail')
        # )

        # copy email to clipboard
        ActionChains(driver).move_to_element(self.driver.find_element_by_id('click-to-copy')).click().perform()
        _mail = pyperclip.paste()
        # _mail = driver.find_element_by_id('mail').text

        print("mail: " + _mail)

        # _mail = WebDriverWait(driver, 8).until(
        #     EC.presence_of_element_located((By.ID, 'current-id'))).get_attribute('value')
        # time.sleep(1)

        # driver.close()

        # switch to instagram tab
        self.driver.switch_to.window((driver.window_handles[0]))

        return _mail

    def fill_activation_code_form(self):

        if self.driver.current_window_handle != driver.window_handles[-1]:  # if driver is in instagram tab, switch it to mail tab
            print("Switching to mail tab")
            self.driver.switch_to.window(driver.window_handles[-1])

            # wait for mail
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]')))

            # open mail
            ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(
                '/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a')).click().perform()

            # get activation code from mail
            _mail_code = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="email_content"]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]'))
            ).text

            print("mail code: ", _mail_code)

            # switch to instagram tab
            self.driver.switch_to.window(self.driver.window_handles[0])

            # enter activation code
            activation_input = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/article/div/div[1]/div[2]/form/div/div[1]/input')
            activation_input.send_keys(_mail_code)
            time.sleep(1)
            activation_input.send_keys(Keys.RETURN)

    def save_credentials_to_file(self, _credentials):
        file_name = 'credentials.txt'
        file = open(file_name, "a+")
        # print('file path: ', str(os.getcwd()) + '\\' + file_name)
        file.write(str(_credentials))
        file.write('\n')
        file.close()

    def fill_registration_form(self, _mail, _full_name, _user_name, _password):
        try:
            mail_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'emailOrPhone')))
            full_name_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'fullName')))
            user_name_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
            password_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password')))

            clear_input(mail_input, full_name_input, user_name_input, password_input)

            mail_input.send_keys(_mail)
            wait_random_time()

            full_name_input.send_keys(_full_name)
            wait_random_time()

            user_name_input.send_keys(_user_name)
            wait_random_time()

            password_input.send_keys(_password)
            wait_random_time(1, 3)
            # ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[7]/div/button')).click().perform()
            password_input.send_keys(Keys.RETURN)
            wait_random_time()

        except Exception as ex:
            print(ex)
            driver.quit()

    def choose_random_value_from_picklist(options_list, is_year_picklist=False):
        global driver

        random.seed()

        # making sure the age is >= 18
        if is_year_picklist:
            del options_list[0:18]

        picked_option = random.choice(options_list)
        print("\npicked option value: ", picked_option.text)
        picked_option.click()

    def fill_birthday_form():
        global driver

        if driver.current_url == 'https://www.instagram.com/accounts/emailsignup/':
            WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.XPATH,
                                                '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[3]/select'))
            )

            year_options = driver.find_elements_by_xpath(
                '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[3]/select/option')
            choose_random_value_from_picklist(year_options, is_year_picklist=True)
            wait_random_time()

            month_options = driver.find_elements_by_xpath(
                '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[1]/select/option')
            choose_random_value_from_picklist(month_options)
            wait_random_time()

            month_day_options = driver.find_elements_by_xpath(
                '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[2]/select/option')
            choose_random_value_from_picklist(month_day_options)
            wait_random_time()

            ActionChains(driver).move_to_element(driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/div[6]/button')).click().perform()


print_current_action('Starting the browser')
driver = get_driver()
print_action_result()

print('Browser session id: ', driver.session_id)
start_url = "https://www.instagram.com/accounts/emailsignup/"

print("Start page URL: " + start_url)
driver.get(start_url)
print_action_result()

print_current_action("Creating User credentials")
full_name = get_random_fullname()
user_name = generate_username(full_name)
password = generate_password()
mail = get_random_mail()
print_action_result()

# debug - instead of getMail
# driver.switch_to.window(driver.window_handles[0])

print_current_action("Filling registration form")
fill_registration_form(mail, full_name, user_name, password)
print_action_result()

credentials = {
    "mail": mail,
    "full_name": full_name,
    "user_name": user_name,
    "password": password
}
print('User credentials: ', credentials)

print_current_action("Saving User credentials to file")
save_credentials_to_file(credentials)
print_action_result()

print_current_action("Filling birthday form")
fill_birthday_form()
print_action_result()

print_current_action("Getting mail activation code")
fill_activation_code_form()

# sleepAndQuit(7)
