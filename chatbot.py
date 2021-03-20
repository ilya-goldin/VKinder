import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import group_token as token
from random import randrange


class ChatBot:
    def __init__(self):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message: str):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7)})

    def requests_data(self, request: str, user_id):
        if request == 'bdate':
            self.write_msg(user_id, 'Какой возраст ищем?'
                                    '\nВведите цифру')
        if request == 'city':
            self.write_msg(user_id, 'В каком городе искать?'
                                    '\nВведите название города')
        if request == 'sex':
            self.write_msg(user_id, 'Какого пола ищем?'
                                    '\nВведите одну цифру:'
                                    '\n1 — женский'
                                    '\n2 — мужской')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event.text

    def search(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == "поиск" or event.text == "Поиск":
                    return self.get_user_id(event.user_id)
                else:
                    self.write_msg(event.user_id, 'Для начала работы с ботом введите "Поиск"')

    def get_user_id(self, user_id):
        self.write_msg(user_id, "Введите имя пользователя или id, для которого нужно "
                                "выполнить поиск")
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event.text, event.user_id

    def attach_image(self, user_id, list_of_images, text):
        import requests
        attachments = []
        upload = vk_api.VkUpload(self.vk)
        for img in list_of_images:
            image = requests.session().get(img, stream=True)
            photo = upload.photo_messages(photos=image.raw)[0]
            attachments.append(
                'photo{}_{}'.format(photo['owner_id'], photo['id'])
            )
        self.vk.method('messages.send', {'user_id': user_id,
                                         'attachment': ','.join(attachments),
                                         'message': text,
                                         'random_id': randrange(10 ** 7)})

