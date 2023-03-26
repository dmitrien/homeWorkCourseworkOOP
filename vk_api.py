
import urllib
import requests as requests

class VKdownoloader:
    def __init__(self, token_path):
        with open(token_path, 'r') as file_object:
            self.tokenVK = file_object.read().strip()

        self.HOST = 'https://api.vk.com/method'
    # Получаем user_id по user_ids
    def get_user_id(self, user_ids):
        params = {
            'user_ids': user_ids,
            'access_token': self.tokenVK,
            'v': '5.131'
        }
        res = requests.get(f'{self.HOST}/users.get', params=params)
        data = res.json()

        return (user_id['id'] for user_id in data['response'])

    # Получаем фото последних загруженных аватарок по умолчанию 5 (numbers_of_photos)
    def get_user_photo(self, user_ids, numbers_of_photos=5):
        params = {
            'owner_id': self.get_user_id(user_ids),
            'album_id': 'profile',
            'photo_sizes': True,
            'extended': True,
            'access_token': self.tokenVK,
            'v': '5.131'
        }
        resPhoto = requests.get(f'{self.HOST}/photos.get', params=params)
        data = resPhoto.json()
        all_photo = data['response']['items']
        json_info = []
        for photo in all_photo[-numbers_of_photos:]:
            max_height = max(dict_h['height'] for dict_h in photo['sizes'])
            max_width = max(dict_w['width'] for dict_w in photo['sizes'])
            count_likes = photo['likes']['count']
            for photo_max in photo['sizes']:
                if photo_max['height'] == max_height and photo_max['width'] == max_width:
                    name_sizes = photo_max['type']
                    link_photo = photo_max['url']
                    info_photo = {
                        'size': name_sizes,
                        'file_name': count_likes,
                        'url_photo': link_photo

                    }
                    json_info.append(info_photo)
                    break
            urllib.request.urlretrieve(info_photo['url_photo'], str(info_photo['file_name']) + '.jpg')

        return json_info