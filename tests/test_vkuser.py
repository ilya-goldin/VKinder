import json
import unittest
import vkuser


class TestVK(unittest.TestCase):
    def test_create_user(self):
        user = vkuser.VKUser(1, 321, 0, True)
        self.assertEqual(36, user.age)
        self.assertEqual(2, user.city)
        self.assertEqual('durov', user.domain)
        self.assertEqual('Павел', user.first_name)
        self.assertEqual('Дуров', user.last_name)
        self.assertEqual(1, user.sex)
        self.assertTrue(user.user_status)

    def test_get_city(self):
        user = vkuser.VKUser(1, 321, 0, True)
        city = user.get_city('Пермь')
        self.assertEqual(110, city)

    def test_get_profile_photos(self):
        user = vkuser.VKUser(1, 321, 0, True)
        with open('photos.json') as file:
            our_photos = json.load(file)
        photos = user.get_profile_photos(1)
        self.assertEqual(our_photos, photos)
