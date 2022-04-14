import os
import string
import random
import requests
from datetime import datetime


class YandexDisk:
    def __init__(self, api_token):
        self.url = 'https://cloud-api.yandex.net/v1/disk/'
        self.headers = {'Authorization': f'OAuth {api_token}'}
        self.delete_days = 10

    def upload_file(self, folder, file):
        params = {'path': f'disk:/{file}', 'overwrite': 'false'}
        response = requests.get(self.url + 'resources/upload', params=params, headers=self.headers)
        with open(f'{folder}/{file}.zip', 'rb') as f:
            requests.put(response.json()['href'], f)
        if response.status_code == 200:
            return f'Архив "{file}" успешно выгружен в Яндекс диск.'
        else:
            return 'Что-то не так'

    def publish_file(self, file):
        params = {'path': f'disk:/{file}'}
        response = requests.put(self.url + 'resources/publish', params=params, headers=self.headers)
        if response.status_code == 200:
            return f'К архиву "{file}" успешно открыт доступ.'
        else:
            return 'Что-то не так'

    def get_public_link(self, file):
        params = {'limit': 100000}
        response = requests.get(self.url + 'resources/files', params=params, headers=self.headers).json()
        for line in response['items']:
            if line['name'] == file:
                return line['public_url']

    def auto_clean(self):
        response = requests.get(self.url + 'resources/files', headers=self.headers).json()
        if len(response['items']) == 0:
            pass
        else:
            for line in response['items']:
                file_name = line['name']
                file_created = datetime.strptime(line['created'].split('T')[0], '%Y-%m-%d')
                days_number = (datetime.now() - file_created).days
                try:
                    if days_number > self.delete_days:
                        self.delete_file(file_name)
                except KeyError:
                    pass

    def delete_file(self, file):  # file = 'disk:/599248'
        params = {'path': f'{file}', 'permanently': 'true'}
        response = requests.delete(self.url + 'resources', params=params, headers=self.headers)
        if response.status_code == 204:
            return f'Архив "{file}" успешно удалён.'


class ZipArchiver:
    def __init__(self, folder):
        self.folder = folder
        self.name = str(PassGen().pass_gen(length=6, method=['digits']))
        self.password = PassGen().pass_gen(length=25, method=['lowercase', 'uppercase', 'digits'])

    def move_to_archive(self):
        try:
            files = os.listdir(self.folder)
            if len(files) == 0:
                return False
        except FileNotFoundError:
            return False

        os.system(f'cd {self.folder} && zip -P {self.password} {self.name}.zip *')
        with open(f'{self.folder}/{self.name}.txt', 'w') as f:
            f.write(f'Password - {str(self.password)}\n\n')
            for file in files:
                if file.startswith('.'):
                    pass
                else:
                    os.remove(f'{self.folder}/{file}')
                    f.write(f'{str(file)}\n')
            f.write('\nLink active for 10 days')
        return f'{self.name}'


class PassGen:
    def pass_gen(self, length=8, method=None):
        """String.lowercase, uppercase, digits, punctuation."""
        if method is None:
            method = ['lowercase', 'uppercase', 'digits', 'punctuation']
        pwd = []
        for i in range(length):
            choice = random.choice(method)
            if choice == "lowercase":
                pwd.append(random.choice(string.ascii_lowercase))
            if choice == "uppercase":
                pwd.append(random.choice(string.ascii_uppercase))
            if choice == "digits":
                pwd.append(random.choice(string.digits))
            if choice == "punctuation":
                pwd.append(random.choice(string.punctuation))
        random.shuffle(pwd)
        return ''.join(pwd)


def main():
    pass


if __name__ == '__main__':
    main()
