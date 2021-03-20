import vk_api
import json
from os.path import exists


class VkAuth:
    def __init__(self):
        if exists('vk_config.v2.json'):
            with open('vk_config.v2.json', 'r', encoding='utf-8') as file:
                config = json.load(file)
            login = list(config.keys())[0]
            app = list(config[login]['token'].keys())[0]
            scope = list(config[login]['token'][app].keys())[0]
            self.token = config[login]['token'][app][scope]['access_token']
            self.email = config[login]['token'][app][scope]['email']
            self.user_id = config[login]['token'][app][scope]['user_id']
        else:
            self.auth()

    def auth_handler(self):
        key = input("Enter authentication code: ")
        remember_device = True
        return key, remember_device

    def auth(self):
        login = input('Enter login: ')
        password = input('Enter password: ')
        vk_session = vk_api.VkApi(
            login, password,
            auth_handler=self.auth_handler
        )
        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)


if __name__ == '__main__':
    x = VkAuth()
    print(x.token, x.email, x.user_id)
