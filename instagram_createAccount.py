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

from Account import Account
from DriverUtils import DriverUtils


class RegistrationDriver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # PROXY = "147.135.7.122:3128"
        options.add_argument("accept-language=en-US")  # set english browser language
        # options.add_argument("--start-maximized")  # set full screen browser
        # options.add_argument('--proxy-server=%s' % PROXY)  # set proxy
        options.add_argument("--disable-blink-features=AutomationControlled")  # disables "automated" pop-up, also helps not getting detected (or not), doesnt work hehe

        self.driver = webdriver.Chrome(options=options)

    def open_start_page(self, url):
        DriverUtils.print_current_action("Entering URL: " + url)
        try:
            self.driver.get(url)
        except Exception:
            DriverUtils.print_action_result(False)
            self.driver.quit()
        else:
            DriverUtils.print_action_result()

    def close_browser(self):
        DriverUtils.print_current_action("Closing browser")
        self.driver.quit()
        DriverUtils.print_action_result()

    def generate_id(self, size=4):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def generate_password(self, size=10):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

    def generate_username(self, _full_name):
        return _full_name.replace(" ", ".") + '.' + self.generate_id()

    def get_random_fullname(self):
        try:
            self.driver.execute_script('window.open("https://www.name-generator.org.uk/quick/");')

            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[-1])

                _full_name = WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[3]/div/div/form/div[1]'))).text

                if '-' in _full_name:
                    _full_name = _full_name.split('-')[1]

                return _full_name
        except Exception as e:
            print(e)
            self.driver.quit()

    def get_random_mail(self):
        mail_url = 'https://temp-mail.org/pl/'

        try:
            self.driver.get(mail_url)
            if len(self.driver.window_handles) > 1:

                # switch to mail tab
                self.driver.switch_to.window(self.driver.window_handles[-1])

                # inside the second tab
                reset_button = WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.ID, 'click-to-delete')))
                reset_button.click()

                time.sleep(5)

                # copy email to clipboard
                ActionChains(self.driver).move_to_element(self.driver.find_element_by_id('click-to-copy')).click().perform()
                mail = pyperclip.paste()

                # switch back to instagram tab
                self.driver.switch_to.window((self.driver.window_handles[0]))

                return mail
        except Exception as e:
            print(e)
            self.driver.quit()

    def fill_activation_code_form(self):
        DriverUtils.print_current_action("Filling activation code form")
        try:
            if self.driver.current_window_handle != self.driver.window_handles[-1]:  # if driver is in instagram tab, switch it to mail tab
                self.driver.switch_to.window(self.driver.window_handles[-1])

                # wait for 2 minutes for mail to read activation code from it
                WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]')))

                # open mail
                ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(
                    '/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a')).click().perform()

                # get activation code from the mail
                _mail_code = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//*[@id="email_content"]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]'))
                ).text


                # switch to instagram tab
                self.driver.switch_to.window(self.driver.window_handles[0])

                # enter activation code
                activation_input = self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/article/div/div[1]/div[2]/form/div/div[1]/input')
                activation_input.send_keys(_mail_code)

                DriverUtils.clear_input(activation_input)

                DriverUtils.wait_random_time()

                activation_input.send_keys(Keys.RETURN)
        except Exception:
            DriverUtils.print_action_result(False)
            self.driver.quit()
        else:
            DriverUtils.print_action_result()

    def fill_registration_form(self, user):
        DriverUtils.print_current_action("Filling registration form")
        try:
            mail_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'emailOrPhone')))
            full_name_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'fullName')))
            user_name_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
            password_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'password')))

            DriverUtils.clear_input(mail_input, full_name_input, user_name_input, password_input)

            mail_input.send_keys(user.get_mail())
            DriverUtils.wait_random_time()

            full_name_input.send_keys(user.get_full_name())
            DriverUtils.wait_random_time()

            user_name_input.send_keys(user.get_user_name())
            DriverUtils.wait_random_time()

            password_input.send_keys(user.get_password())
            DriverUtils.wait_random_time()

            password_input.send_keys(Keys.RETURN)

        except Exception as e:
            DriverUtils.print_action_result(False)
            self.driver.quit()
        else:
            DriverUtils.print_action_result()

    def choose_random_value_from_picklist(self, options_list, is_year_picklist=False):
        random.seed()

        # making sure the age is >= 18 if the list is a years list
        if is_year_picklist:
            del options_list[0:18]

        picked_option = random.choice(options_list)
        picked_option.click()

    def fill_birthday_form(self):

        DriverUtils.print_current_action("Filling birthday form")
        try:
            if self.driver.current_url == 'https://www.instagram.com/accounts/emailsignup/':
                WebDriverWait(self.driver, 7).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[3]/select'))
                )

                year_options = self.driver.find_elements_by_xpath(
                    '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[3]/select/option')
                self.choose_random_value_from_picklist(year_options, is_year_picklist=True)
                DriverUtils.wait_random_time()

                month_options = self.driver.find_elements_by_xpath(
                    '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[1]/select/option')
                self.choose_random_value_from_picklist(month_options)
                DriverUtils.wait_random_time()

                month_day_options = self.driver.find_elements_by_xpath(
                    '/html/body/div[1]/section/main/div/article/div/div[1]/div/div[4]/div/div/span/span[2]/select/option')
                self.choose_random_value_from_picklist(month_day_options)
                DriverUtils.wait_random_time()

                ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/div[6]/button')).click().perform()
        except Exception as e:
            DriverUtils.print_action_result(False)
            self.driver.quit()
        else:
            DriverUtils.print_action_result()


def main():
    driver_reg = RegistrationDriver()

    start_url = "https://www.instagram.com/accounts/emailsignup/"
    driver_reg.open_start_page(start_url)

    # creating user credentials
    full_name = driver_reg.get_random_fullname()
    user_name = driver_reg.generate_username(full_name)
    password = driver_reg.generate_password()
    mail = driver_reg.get_random_mail()

    user_account = Account(mail, full_name, user_name, password)
    user_account.save_credentials_to_file()

    driver_reg.fill_registration_form(user_account)

    driver_reg.fill_birthday_form()
    driver_reg.fill_activation_code_form()


if __name__ == "__main__":
    main()

    while 1:
        pass

