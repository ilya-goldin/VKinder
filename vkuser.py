import requests
import config
from time import sleep
from datetime import datetime as dt


class VKUser:
    main_url = 'https://api.vk.com/method/'
    version = '5.130'
    params = {
        'access_token': config.user_token,
        'v': version}

    def __init__(self, user_id, request_user_id, offset: int, new_user: bool = True):
        self.user_id = user_id
        self.request_user_id = request_user_id
        self.first_name = None
        self.last_name = None
        if new_user:
            self.user_status = self.get_user()
        else:
            self.user_status = True
        self.offset = offset

    def get_user(self):
        check_params = {'user_ids': self.user_id,
                        'fields': 'bdate,city,sex,domain'}
        response = requests.get(
            self.main_url + 'users.get',
            params=self.params | check_params).json()
        if 'error' in response.keys():
            print(response['error']['error_msg'])
            return False
        response = response['response'][0]
        self.user_id = int(response['id'])
        self.first_name = response['first_name']
        self.last_name = response['last_name']
        self.domain = response['domain']

        requset_list = []
        if 'bdate' in response.keys():
            if len(response['bdate']) >= 8:
                self.age = (dt.now() - dt.strptime(response['bdate'], '%d.%m.%Y')).days // 365
            else:
                requset_list.append('bdate')
        else:
            requset_list.append('bdate')
        if 'city' in response.keys():
            self.city = response['city']['id']
        else:
            requset_list.append('city')
        if 'sex' in response.keys() and response['sex']:
            self.sex = 2 if (response['sex'] == 1) else 1
        else:
            requset_list.append('sex')

        if requset_list:
            return requset_list, response['is_closed']
        else:
            return not response['is_closed']

    def get_city(self, city_name: str, country_id: int = 1):
        params = {'country_id': country_id,
                  'q': city_name,
                  'count': 1}
        response = requests.get(self.main_url + 'database.getCities',
                                params=self.params | params).json()
        if 'error' in response.keys():
            print(response['error']['error_msg'])
            return False
        return int(response['response']['items'][0]['id'])

    def get_profile_photos(self, user_id):
        profile_photo_params = {'owner_id': user_id,
                                'album_id': 'profile',
                                'rev': 1,
                                'extended': 1,
                                'photo_sizes': 1}
        response = requests.get(self.main_url + 'photos.get',
                                params=self.params | profile_photo_params).json()
        if 'error' in response.keys():
            print(response['error']['error_msg'])
            return False
        if 'response' in response.keys() and response['response']['count'] > 0:
            result: list = response['response']['items']
            result.sort(key=lambda likes: likes['likes']['count'])
            result = result[:3]
            for i in result:
                i['sizes'] = i['sizes'][-1]
            return result
        else:
            return response

    def __iter__(self):
        return self

    def __next__(self):
        match_params = {'fields': 'domain',
                        'city': self.city,
                        'offset': self.offset,
                        'count': 10,
                        'sex': self.sex,
                        'age_from': self.age,
                        'age_to': self.age,
                        'status': 6,
                        'has_photo': 1}
        response = requests.get(
            self.main_url + 'users.search',
            params=self.params | match_params
        ).json()
        if 'error' in response.keys():
            return response
        sleep(0.3)
        if 'response' in response.keys():
            if len(response['response']['items']):
                self.current_search = response['response']['items']
                self.offset += 1
                if self.offset == response['response']['count']:
                    raise StopIteration
                return self.current_search
        return response

