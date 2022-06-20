class MainStrings:
    def __init__(self):
        self.no_time = 'Вы исчерпали свой лимит.\n Эта функция работает пробно, вы можете написать разработчику (@DrGsan). Спасибо)'
        self.max_length = 'Оказалось, что я не могу слушать аудиосообщения > 30 секунд (Спасибо Яндексу). Но скоро я научусь, а пока слушай всё сам.'
        self.no_words = 'Не смог ничего распознать'
        self.access_error = 'У вас нет доступа к этой команде'

        self.button_weather = 'Введи название города (или отправьте геопозицию):'
        self.weather_empty = 'На сегодня погода иcчерпала свой лимит запросов'
        self.weather_error = 'Некорректно введен город'
        self.button_translator = 'Напиши слово или фразу для перевода.'
        self.button_transliterate = 'Напиши слово или фразу'
        self.button_passport = 'Напиши Имя и Фамилию'
        self.passport = 'Транслитерация имени и фамилии для загранпаспорта' \
                        'заменяет буквы русского алфавита буквами латинского алфавита по правилам,' \
                        'установленным приказом МВД России от 27 ноября 2017 г. N 889 "Об утверждении ' \
                        'Административного регламента Министерства внутренних дел Российской Федерации ' \
                        'по предоставлению государственной услуги по оформлению и выдаче паспортов гражданина ' \
                        'Российской Федерации, удостоверяющих личность гражданина Российской Федерации за ' \
                        'пределами территории Российской Федерации, содержащих электронный носитель информации". ' \
                        '(Приложение N 2)'
        self.default_error = 'Что-то не так'
        self.access_error = 'У вас нет доступа к этой команде'
        self.help = 'admin - Получить список команд (только для админа)\n' \
                    'id - Узнать свой id и группы (если в группе)\n' \
                    'currency - Курс Валют ($, €)\n' \
                    'balance - Запросить свой баланс (кол-во секунд)\n' \
                    'disk - Получить ссылку на архив (перед этим отправить файлы в личку боту)\n' \
                    'weather - Погода\n' \
                    'translate - Переводчик (ru-en, en-ru)\n' \
                    'transliterate - Сообщение иероглифами\n' \
                    'passport - Транслитерация ФИ для загранпаспорта'
