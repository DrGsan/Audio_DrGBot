class MainStrings:
    def __init__(self):
        self.no_time = 'Вы исчерпали свой лимит.\n Эта функция работает пробно, вы можете написать разработчику (@DrGsan) и он вам обнулит результат и добавит ещё 180 секунд. Спасибо)'
        self.max_length = 'Оказалось, что я не могу слушать сообщения больше 30 секунд (Спасибо Яндексу). Но скоро я научусь, а пока слушай всё сам.'
        self.no_words = 'Не смог ничего распознать'
        self.access_error = 'У вас нет доступа к этой команде'

        self.button_weather = 'Введи название города (или отправьте геопозицию):'
        self.weather_empty = 'На сегодня погода ичерпала свой лимит запросов'
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
        self.button_news = 'Введите текст:'
        self.news_done = 'Новости отправлены'
        self.news_no_file = 'У вас ещё нет списка пользователей.'
        self.default_error = 'Что-то не так'
        self.save = 'Введите текст для сохранения в файл temp/note.txt'
        self.save_done = 'Текст сохранен'
        self.access_error = 'У вас нет доступа к этой команде'
        self.logs = 'Сейчас выведу логи'
        self.logs_empty = 'Логи пусты'
        self.logs_file_none = 'Ещё никто не запускал бота. Файл логов отсутствует'
        self.help = 'Функционал:\n' \
                    '- запрос своего id;' \
                    '- отправляет погоду по геопозиции или через название города;\n' \
                    '- переводчик (автоматически переводит язык с ru-en и en-ru)\n' \
                    '- запрос курса валют $, € (ожидание до 1 минуты);\n' \
                    '- TRANSLITERATE (попробуйте);\n' \
                    '- Транслитерация ФИ для загранпаспорта;\n' \
                    '- генерирует случайное число  (1-100);\n' \
                    '- при отправке геопозиции, координаты;\n' \
                    '- при отправке стикера, отобразится его id.'