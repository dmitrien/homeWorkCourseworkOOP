from vk_api import VKdownoloader
from yandex_disk import YaUploader

if __name__=='__main__':
    downloader = VKdownoloader('tokenVK.txt')
    info_file_downloader = downloader.get_user_photo('dmitrien96')
    uploader = YaUploader('tokenYD.txt')
    result = uploader.uploadFile(info_file_downloader)
