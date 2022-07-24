import requests
import geocoder

URL = 'https://api.weather.yandex.ru/v1/informers/'


class Weather:
    def __init__(self, api):
        self.api = api

    def get_weather(self, user, city_name):
        if type(city_name) == str:
            g = geocoder.geonames(city_name, key=user, lang='ru-RU')
            city_lat = g.latlng[0]
            city_lon = g.latlng[1]
        elif type(city_name) == list:
            city_lat = city_name[0]
            city_lon = city_name[1]
        else:
            print('We have a problem')

        params = {'lat': city_lat, 'lon': city_lon, 'lang': 'ru_RU'}
        headers = {'X-Yandex-API-Key': self.api}
        result = requests.get(URL, params=params, headers=headers).json()

        WEATHER_TRANSLATE = {
            'clear': 'Ясно ☀',
            'partly-cloudy': 'Малооблачно ⛅',
            'cloudy': 'Облачно с прояснениями 🌥',
            'overcast': 'Пасмурно ☁',
            'partly-cloudy-and-light-rain': 'Небольшой дождь 🌧',
            'partly-cloudy-and-rain': 'Дождь 🌧',
            'overcast-and-rain': 'Сильный дождь 🌧🌧',
            'overcast-thunderstorms-with-rain': 'Сильный дождь, гроза 🌩',
            'cloudy-and-light-rain': 'Небольшой дождь 🌧',
            'overcast-and-light-rain': 'Небольшой дождь 🌧',
            'cloudy-and-rain': 'Дождь 🌧',
            'overcast-and-wet-snow': 'Дождь со снегом 🌨',
            'partly-cloudy-and-light-snow': 'Небольшой снег 🌨',
            'partly-cloudy-and-snow': 'Снег 🌨',
            'overcast-and-snow': 'Снегопад 🌨',
            'cloudy-and-light-snow': 'Небольшой снег 🌨',
            'overcast-and-light-snow': 'Небольшой снег 🌨',
            'cloudy-and-snow': 'Снег 🌨'}
        DAY_TRANSLATE = {
            'night': 'ночь',
            'morning': 'утро',
            'day': 'день',
            'evening': 'вечер',
        }

        WEATHER = {
            'now': {
                'temp': result['fact']['temp'],
                'temp_feels_like': result['fact']['feels_like'],
                'condition': WEATHER_TRANSLATE[result['fact']['condition']],
                'wind_speed': result['fact']['wind_speed'],
                'wind_gust': result['fact']['wind_gust'],
                'pressure': result['fact']['pressure_mm'],
                'humidity': result['fact']['humidity'],
            },
            'forecast': {}}

        for i in range(len(result['forecast']['parts'])):
            WEATHER['forecast'][i] = {
                'part_name': DAY_TRANSLATE[result['forecast']['parts'][i]['part_name']],
                'temp_min': result['forecast']['parts'][i]['temp_min'],
                'temp_max': result['forecast']['parts'][i]['temp_max'],
                'temp_feels_like': result['forecast']['parts'][i]['feels_like'],
                'condition': WEATHER_TRANSLATE[result['forecast']['parts'][i]['condition']],
                'wind_speed': result['forecast']['parts'][i]['wind_speed'],
                'wind_gust': result['forecast']['parts'][i]['wind_gust'],
                'pressure': result['forecast']['parts'][i]['pressure_mm'],
                'humidity': result['forecast']['parts'][i]['humidity'],
                'prec_mm': result['forecast']['parts'][i]['prec_mm'],
                'prec_period': int(int(result['forecast']['parts'][i]['prec_period']) / 60),
                'prec_prob': result['forecast']['parts'][i]['prec_prob'],
            }

        if type(city_name) == str:
            enter = 'Погода в городе {} сейчас:\n'.format(city_name)
        elif type(city_name) == list:
            enter = 'Погода по вашим координатам сейчас:\n'

        now = '{}\n' \
              'Температура {}°С (ощущается как {}°С)\n' \
              'Ветер {} м/c(порывы до {} м/c)\n' \
              'Давление  {} мм.рт.ст., влажность {}%'.format(
            WEATHER['now']['condition'], WEATHER['now']['temp'], WEATHER['now']['temp_feels_like'],
            WEATHER['now']['wind_speed'], WEATHER['now']['wind_gust'], WEATHER['now']['pressure'],
            WEATHER['now']['humidity'])

        forecast = ""
        for i in range(len(WEATHER['forecast'])):
            forecast += '\n\n' \
                        'Прогноз на {}:\n' \
                        '{}\n' \
                        'Температура {}-{}°С(ощущается как {}°С)' \
                        '\nВетер {} м/c (порывы до {} м/c)\n' \
                        'Давление {} мм.рт.ст., влажность {}%\n' \
                        'Осадки {} мм на протяжении {} часов с вероятностью {}%'.format(
                WEATHER['forecast'][i]['part_name'],
                WEATHER['forecast'][i]['condition'],
                WEATHER['forecast'][i]['temp_min'], WEATHER['forecast'][i]['temp_max'],
                WEATHER['forecast'][i]['temp_feels_like'],
                WEATHER['forecast'][i]['wind_speed'], WEATHER['forecast'][i]['wind_gust'],
                WEATHER['forecast'][i]['pressure'], WEATHER['forecast'][i]['humidity'],
                WEATHER['forecast'][i]['prec_mm'], WEATHER['forecast'][i]['prec_period'],
                WEATHER['forecast'][i]['prec_prob'])
        return enter + now + forecast
