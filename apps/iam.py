import os
import json
import requests


class IAM_token:
    def __init__(self, oauth_token):
        self.oauth_token = oauth_token

    def file_exist(self, iam_file):
        try:
            os.stat(iam_file)
        except OSError:
            return False
        return True

    def create_token(self, iam_file):
        params = {'yandexPassportOauthToken': self.oauth_token}
        response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)
        decode_response = response.content.decode('UTF-8')
        text = json.loads(decode_response)
        iam_token = text.get('iamToken')
        with open(iam_file, 'w') as f:
            f.write(iam_token)
        return iam_token


def main():
    pass


if __name__ == '__main__':
    main()
