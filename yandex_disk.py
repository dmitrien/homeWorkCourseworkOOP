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
            path_to_file = str(file['file_name']) + '.jpg'
            params = {'path': 'VKPhoto/' + path_to_file, 'overwrite': 'true'}
            response = requests.get(upload_url, headers=headers, params=params)
            data = response.json()
            href = data.get('href')
            response = requests.put(href, data=path_to_file)
            if response.status_code == 201:
                info_file = {
                    'file_name': path_to_file,
                    'size': file['size']
                }
                print(f'Файл успешно загружен: {path_to_file}')
                loger_json['successfull_uploaded'].append(info_file)

        with open('loger_json.json', 'w', encoding='utf-8') as json_file:
                   json.dump(loger_json, json_file)