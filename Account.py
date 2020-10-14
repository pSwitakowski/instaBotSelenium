import json


class Account:
    def __init__(self, mail, full_name, user_name, password):
        self.mail = mail
        self.full_name = full_name
        self.user_name = user_name
        self.password = password

    def save_credentials_to_file(self):
        try:
            file_name = 'users.txt'
            file = open(file_name, "a+")

            json_acc = json.dumps(self.__dict__)

            file.write(json_acc)
            file.write('\n')
            file.close()
        except FileNotFoundError as e:
            print(e)

    def get_mail(self):
        return self.mail

    def get_full_name(self):
        return self.full_name

    def get_user_name(self):
        return self.user_name

    def get_password(self):
        return self.password

    def set_mail(self, mail):
        self.mail = mail

    def set_full_name(self, full_name):
        self.full_name = full_name

    def set_user_name(self, user_name):
        self.user_name = user_name

    def set_password(self, password):
        self.password = password