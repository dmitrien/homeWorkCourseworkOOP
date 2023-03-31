import json
import requests as requests

class YaUploader:
    def __init__(self, token_path):
        with open(token_path, 'r') as file_object:
            self.tokenYD = file_object.read().strip()

    # Загружаем полученные файлы на YandexDisk
    def uploadFile(self, json_info_photo):
        host = 'https://cloud-api.yandex.net'
        upload_url = host + '/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.tokenYD)
        }
        requests.put(host + '/v1/disk/resources?path=VKPhoto', headers=headers)
        # Создаем логер для скачанных аватарок
        loger_json = {}
        loger_json['successfull_uploaded'] = []
        uploaded_files = []
        for name_file in json_info_photo:
            uploaded_files.append(str(name_file['file_name']) + '.jpg')
        print(f'Список загружаемых файлов: {", ".join(uploaded_files)}')
        # Загружаем файлы
        for file in json_info_photo:
            file_name = str(file['file_name']) + '.jpg'
            url_to_file = file['url_photo']
            params = {'url': url_to_file, 'path': 'VKPhoto/' + file_name}
            response = requests.post(upload_url, headers=headers, params=params)
            if response.status_code == 202:
                info_file = {
                    'file_name': file['file_name'],
                    'size': file['size']
                }
                print(f'Файл успешно загружен: {file_name}')
                loger_json['successfull_uploaded'].append(info_file)

        with open('loger_json.json', 'w', encoding='utf-8') as json_file:
                   json.dump(loger_json, json_file)