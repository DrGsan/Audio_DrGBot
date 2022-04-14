#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import urllib

import shutil
# noinspection PyPackageRequirements
import telebot
import requests
import schedule
from threading import Thread

from apps.apps import Apps
from apps.iam import IAM_token
from apps.speech import Speech
from apps.weather import Weather
from apps.currency import currency
from apps.translate import Translate
from apps.transliterate import Transliterate
from apps.ya_disk import YandexDisk, ZipArchiver
from apps.db import work_with_db, get_token, get_groups, is_admin, is_blocked, get_total_audio, update_total_audio, \
    update_is_left

from strings.main_strings import MainStrings

TOKEN = get_token('Audio_DrGBot_API', 'Telegram')
OAUTH_TOKEN = get_token('Oauth_Token', 'Yandex')
FOLDER_ID = get_token('Folder_ID', 'Yandex')
MY_ID = get_token('My_ID', 'Telegram')
YANDEX_WEATHER_API = get_token('Weather_API', 'Yandex')
YA_DISK_TOKEN = get_token('Disk_API', 'Yandex')
GEOCODER_USER = get_token('User_Key', 'GeoCoder')

bot = telebot.TeleBot(TOKEN)


def new_year_msk_function():
    text = 'С Новым Годом Москва!'
    for chat_id in get_groups():
        Apps().send_chat_action(bot, chat_id, text=text)  # Уведомление Chat_Action
        bot.send_message(chat_id, text)


def ya_disk_func():
    YandexDisk(YA_DISK_TOKEN).auto_clean()


def temp_clean():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp/')
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


@bot.message_handler(commands=['start'])
def start_message(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.chat.type == 'private' and is_blocked(message) is False:
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}')


@bot.message_handler(commands=['send_text'])  # Отправка текстовых сообщений в определённый чат
def send_text_to_group(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.chat.type == 'private' and is_admin(message) is True:
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, 'Введите id группы и текст через пробел (пример: -12345 Текст)')
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.register_next_step_handler(message, send_text_message)


def send_text_message(message):
    group_id = str(message.text).split(' ')[0]
    group_text = ' '.join(str(message.text).split(' ')[1:])
    Apps().send_chat_action(bot, chat_id=group_id, text=group_text)  # Уведомление Chat_Action
    bot.send_message(group_id, group_text)


@bot.message_handler(commands=['send_voice'])  # Отправка аудио сообщений в определённый чат
def send_audio_to_group(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.chat.type == 'private' and is_admin(message) is True:
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, 'Введите id группы и текст через пробел (пример: -12345 Текст)')
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, db.get_groups_id('telegram_groups'))
        bot.register_next_step_handler(message, send_audio_message)


def send_audio_message(message):
    group_id = str(message.text).split(' ')[0]
    group_text = ' '.join(str(message.text).split(' ')[1:])
    temp_path = 'temp'
    Apps().make_folder(temp_path)  # Создать папку если она отсутствует
    iam_file = f'{temp_path}/iam.txt'
    output_file = f'{temp_path}/group_output.ogg'
    while True:
        try:
            with open(iam_file, 'r') as f:
                iam_token = f.read()
            break

        except FileNotFoundError:
            IAM_token(OAUTH_TOKEN).create_token(iam_file)
            pass
    with open(output_file, "wb") as f:
        for audio_content in Speech(FOLDER_ID, iam_token).create_voice(group_text):
            f.write(audio_content)

    audio = open(output_file, 'rb')
    Apps().send_chat_action(bot, chat_id=group_id, action='record_audio', text=group_text)  # Уведомление Chat_Action
    bot.send_audio(group_id, audio)
    audio.close()
    os.remove(output_file)


@bot.message_handler(commands=['disk'])
def some(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.chat.type == 'private' and is_blocked(message) is False:
        folder = f'temp/temp_disk_{message.chat.id}'

        file = ZipArchiver(folder).move_to_archive()
        if file is False:
            Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            bot.send_message(message.chat.id, 'Файлы не обнаружены')
        else:
            Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            mes1 = bot.send_message(message.chat.id, f'Архив "{file}" успешно создан.')

            Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            mes2 = bot.send_message(message.chat.id, YandexDisk(YA_DISK_TOKEN).upload_file(folder, file))
            Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            mes3 = bot.send_message(message.chat.id, YandexDisk(YA_DISK_TOKEN).publish_file(file))

            with open(f'{folder}/{file}.txt', 'a') as f:
                f.write(f'\n{YandexDisk(YA_DISK_TOKEN).get_public_link(file)}')

            time.sleep(5)
            os.remove(f'{folder}/{file}.zip')

            Apps().send_chat_action(bot, chat_id=message.chat.id, action='upload_document',
                                    sec=2)  # Уведомление Chat_Action
            doc = bot.send_document(message.chat.id, open(f'{folder}/{file}.txt', 'rb'))
            time.sleep(5)
            os.remove(f'{folder}/{file}.txt')
            mes4 = bot.send_message(message.chat.id, 'У Вас есть 5 минут на скачивание txt файла с ссылкой на архив ')
            time.sleep(10)
            bot.delete_message(message.chat.id, mes1.message_id)
            bot.delete_message(message.chat.id, mes2.message_id)
            bot.delete_message(message.chat.id, mes3.message_id)
            time.sleep(60 * 4)
            mes5 = bot.send_message(message.chat.id, 'Осталась 1 минута')
            time.sleep(50)
            bot.delete_message(message.chat.id, mes5.message_id)
            bot.delete_message(message.chat.id, doc.message_id)
            bot.delete_message(message.chat.id, mes4.message_id)


@bot.message_handler(commands=['currency'])  # Курс Валют
def currency_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if is_blocked(message) is False:
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, f'Текущий курс валют:\n$ - {currency("USD")} ₽\n€ - {currency("EUR")} ₽')


@bot.message_handler(commands=['id'])  # Отправка id пользователя и группы (если бот в группе)
def id_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if is_blocked(message) is False:
        user_id = str(message.from_user.id)
        group_id = str(message.chat.id)
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        if user_id == group_id:
            bot.send_message(message.chat.id, f'Ваш ID: {user_id}')
        else:
            bot.send_message(message.chat.id, f'Ваш ID: {user_id}\nID группы: {group_id}')


@bot.message_handler(commands=['translate'])  # Переводчик
def translate_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.chat.type == 'private' and is_blocked(message) is False:
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, MainStrings().button_translator)
        bot.register_next_step_handler(message, translate)


def translate(message):
    temp_path = 'temp/'
    Apps().make_folder(temp_path)  # Создать папку если она отсутствует
    iam_file = temp_path + 'iam.txt'
    Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    while True:
        try:
            iam_file = temp_path + 'iam.txt'
            if IAM_token(OAUTH_TOKEN).file_exist(iam_file) is True:
                pass
            else:
                IAM_token(OAUTH_TOKEN).create_token(iam_file)
            with open(iam_file, 'r') as f:
                iam_token = f.read()
            t = Translate(FOLDER_ID, iam_token)
            if t.get_language(message.text) == 'en':
                result = t.get_translation(message.text, 'en', 'ru')
            else:
                result = t.get_translation(message.text, 'ru', 'en')
            bot.send_message(message.chat.id, result)
            break
        except KeyError:
            bot.send_message(message.chat.id, MainStrings().default_error)
            break
        except requests.exceptions.HTTPError:
            IAM_token(OAUTH_TOKEN).create_token(iam_file)


@bot.message_handler(commands=['weather'])  # Погода
def weather_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.chat.type == 'private' and is_blocked(message) is False:
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, MainStrings().button_weather)
        bot.register_next_step_handler(message, weather)


def weather(message):
    w = Weather(YANDEX_WEATHER_API)
    Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    while True:
        try:
            if message.location is None:
                result = w.get_weather(GEOCODER_USER, message.text)
            else:
                geo_location = [message.location.latitude, message.location.longitude]
                result = w.get_weather(GEOCODER_USER, geo_location)
            bot.send_message(message.chat.id, result)
            break
        except KeyError:
            print(MainStrings().weather_empty)
        except BaseException:
            print(MainStrings().weather_error)
            break


@bot.message_handler(commands=['transliterate'])  # Иероглифы
def transliterate_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.chat.type == 'private' and is_blocked(message) is False:
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, MainStrings().button_transliterate)
        bot.register_next_step_handler(message, transliterate_hieroglyphs)


def transliterate_hieroglyphs(message):
    Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    result = Transliterate.transliterate_hieroglyphs(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['passport'])  # Транслитерация имени и фамилии для загранпаспорта
def transliterate_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.chat.type == 'private' and is_blocked(message) is False:
        Apps().send_chat_action(bot, chat_id=message.chat.id, sec=3)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, MainStrings().passport)
        Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        bot.send_message(message.chat.id, MainStrings().button_passport)
        bot.register_next_step_handler(message, transliterate_passport)


def transliterate_passport(message):
    Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    result = Transliterate.transliterate_passport(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(
    content_types=['text', 'audio', 'document', 'photo', 'sticker',
                   'video', 'video_note', 'voice', 'location', 'contact',
                   'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo',
                   'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                   'migrate_from_chat_id', 'pinned_message'])
def handler_content_types(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.content_type == 'voice' and is_blocked(message) is False and message.from_user.is_bot is False:
        if is_admin(message) is True:
            work_with_audio(message)
        else:
            if (get_total_audio(message)) <= 0:
                Apps().send_notification(bot, message, chat_id=MY_ID, action='no_time')
                bot.send_message(message.chat.id, MainStrings().no_time)
            elif message.voice.duration >= 30:
                bot.send_message(message.chat.id, MainStrings().max_length)
            else:
                audio_time = get_total_audio(message) - message.voice.duration
                update_total_audio(message, audio_time)
                work_with_audio(message)

    elif message.from_user.is_bot is False and message.chat.type != 'private':
        if message.content_type == 'new_chat_members':  # Реагирует на уведомление "присоединился к нам"
            if message.json['new_chat_members'][0]['is_bot'] is False:
                update_is_left(message, False)
                Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
                bot.send_message(message.chat.id, f'Добро пожаловать {message.new_chat_members[0].first_name}')
        elif message.content_type == 'left_chat_member':  # Реагирует на уведомление "покинул группу"
            if message.json['left_chat_member']['is_bot'] is False:
                update_is_left(message, True)
                Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
                bot.send_message(message.chat.id, f'До встречи {message.left_chat_member.first_name}.')
        elif message.content_type == 'new_chat_title':
            Apps().echo_voice(bot, message, 'title')  # Отправляет случайное сообщение из title.txt
        elif message.content_type == 'new_chat_photo':
            Apps().echo_voice(bot, message, 'avatar')  # Отправляет случайное сообщение из avatar.txt
        elif message.content_type == 'text':
            if message.reply_to_message is not None and message.reply_to_message.from_user.id == int(
                    TOKEN.split(':')[0]):
                Apps().send_notification(bot, message, chat_id=MY_ID, action='reply_message')

    elif message.from_user.is_bot is False and message.chat.type == 'private':
        if message.content_type == 'document':
            Apps().make_folder('temp/')
            temp_path = f'temp/temp_disk_{message.from_user.id}'
            Apps().make_folder(temp_path)

            file_name = f'{temp_path}/{message.document.file_name}'
            Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            if (message.document.file_size / 1000000) < 21:
                file_info = bot.get_file(message.document.file_id)
                file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
                with open(file_name, 'wb') as f:
                    f.write(file.content)
                mes = bot.send_message(message.chat.id, f'Файл "{message.document.file_name}" успешно загружен.')
                time.sleep(5)
                bot.delete_message(message.chat.id, message.message_id)
                time.sleep(5)
                bot.delete_message(message.chat.id, mes.message_id)
            else:
                bot.send_message(message.chat.id,
                                 f'ОШИБКА API "{message.document.file_name}" > 20mb')
        elif message.content_type == 'sticker' and is_blocked(message) is False:
            Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            bot.send_message(message.chat.id, f'ID стикера: {message.sticker.file_id}')
        elif message.content_type == 'location' and is_blocked(message) is False:
            Apps().send_chat_action(bot, chat_id=message.chat.id, sec=2)  # Уведомление Chat_Action
            bot.send_message(message.chat.id, f'lat = {message.location.latitude}\n'
                                              f'lon = {message.location.longitude}\n'
                                              f'[{message.location.latitude}, {message.location.longitude}]')


def work_with_audio(message):
    temp_path = 'temp/'
    Apps().make_folder(temp_path)  # Создать папку если она отсутствует
    iam_file = f'{temp_path}/iam.txt'
    speech_file = f'{temp_path}/{message.voice.file_id}.ogg'
    file_info = bot.get_file(message.voice.file_id)
    # Отправка на распознавание
    file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
    with open(speech_file, 'wb') as f:
        f.write(file.content)
    while True:
        try:
            with open(f'{temp_path}/iam.txt', 'r') as f:
                iam_token = f.read()
            text = Speech(FOLDER_ID, iam_token).read_voice(speech_file)
            break
        except urllib.error.HTTPError:
            text = Speech(FOLDER_ID, IAM_token(OAUTH_TOKEN).create_token(iam_file)).read_voice(speech_file)
            break
        except FileNotFoundError:
            IAM_token(OAUTH_TOKEN).create_token(iam_file)
            pass
    Apps().send_chat_action(bot, chat_id=message.chat.id, text=text)  # Уведомление Chat_Action
    if len(text) == 0:
        bot.send_message(message.chat.id, MainStrings().no_words)
    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}:\n{text}')
        Apps().echo_voice(bot, message, 'voice')  # Отправляет случайное сообщение из voice.txt
    time.sleep(5)
    os.remove(speech_file)  # Удаляет аудио файл после его преобразования и отправки как текстового сообщения


if __name__ == '__main__':
    if Apps().current_date('%d.%m') == '31.12':
        schedule.every().day.at('00:00').do(new_year_msk_function)
        Thread(target=schedule_checker).start()

    schedule.every().day.at('01:00').do(ya_disk_func)
    schedule.every().day.at('01:00').do(temp_clean)
    Thread(target=schedule_checker).start()

    bot.infinity_polling()