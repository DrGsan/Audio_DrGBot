import requests


class Translate:
    URL = 'https://translate.api.cloud.yandex.net/translate/v2/'

    def __init__(self, folder_id, iam_token):
        self.folder_id = folder_id
        self.iam_token = iam_token

    def get_language(self, text):
        headers = {"Authorization": "Bearer {}".format(self.iam_token)}
        params = {"text": text, "folder_id": self.folder_id}
        response = requests.post(self.URL + 'detect', params=params, headers=headers)
        response.raise_for_status()
        return response.json()["languageCode"]

    def get_translation(self, text, source_lang, target_lang):
        headers = {"Authorization": "Bearer {}".format(self.iam_token)}
        params = {"texts": text, "sourceLanguageCode": source_lang, "targetLanguageCode": target_lang,
                  "folder_id": self.folder_id}
        response = requests.post(self.URL + 'translate', params=params, headers=headers)
        response.raise_for_status()
        translations = response.json()["translations"]
        return translations[0]["text"].replace("+", " ")


def main():
    pass


if __name__ == '__main__':
    main()
