import json
import requests
import urllib.request


class Speech:
    def __init__(self, folder_id, iam_token):
        self.folder_id = folder_id
        self.iam_token = iam_token

    def read_voice(self, speech_file):
        with open(speech_file, 'rb') as f:
            data = f.read()

        params = '&'.join(['topic=general', 'folderId=%s' % self.folder_id, 'lang=ru-RU'])
        url = urllib.request.Request('https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s' % params, data=data)
        url.add_header('Authorization', 'Bearer %s' % self.iam_token)

        responseData = urllib.request.urlopen(url).read().decode('UTF-8')
        decodedData = json.loads(responseData)

        if decodedData.get('error_code') is None:
            return decodedData.get('result')

    def create_voice(self, text):
        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        headers = {'Authorization': 'Bearer ' + self.iam_token}

        data = {
            'text': text,
            'lang': 'ru-RU',
            'voice': 'ermil:rc',
            'folderId': self.folder_id
        }

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError('Invalid response received: code: %d, message: %s' % (resp.status_code, resp.text))

            for chunk in resp.iter_content(chunk_size=None):
                yield chunk
