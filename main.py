#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import urllib

import shutil
import asyncio
# noinspection PyPackageRequirements
from telebot.async_telebot import AsyncTeleBot
import requests
import aioschedule
from apps.apps import Apps
from apps.iam import IAM_token
from apps.vpn import VPN
from apps.speech import Speech
from apps.weather import Weather
from apps.currency import currency
from apps.translate import Translate
from apps.transliterate import Transliterate
from apps.ya_disk import YandexDisk, ZipArchiver, PassGen
from apps.db import work_with_db, get_token, get_groups, get_total_audio, update_total_audio, update_is_left, \
    disk_insert, auto_clean_disk_files, log_insert, vpn_insert, is_vpn_user_exist, get_cell

from strings.main_strings import MainStrings

from config import *

TOKEN = os.environ['TOKEN']
OAUTH_TOKEN = get_token('Oauth_Token', 'Yandex')
FOLDER_ID = get_token('Folder_ID', 'Yandex')
MY_ID = get_token('My_ID', 'Telegram')
YANDEX_WEATHER_API = get_token('Weather_API', 'Yandex')
YA_DISK_TOKEN = get_token('Disk_API', 'Yandex')
GEOCODER_USER = get_token('User_Key', 'GeoCoder')

bot = AsyncTeleBot(TOKEN)


async def new_year_msk_function():
    text = 'С Новым Годом Москва!'
    for chat_id in get_groups():
        await Apps().send_chat_action(bot, chat_id, text=text)  # Уведомление Chat_Action
        await bot.send_message(chat_id, text)


def clean_disk():
    auto_clean_disk_files(YandexDisk, YA_DISK_TOKEN)


def temp_clean():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp/')
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def get_status(message):
    if get_cell(message, 'is_blocked') is True:  # Заблокирован == True
        return 0  # Blocked
    else:
        if get_cell(message, 'is_admin') is True:  # Администратор == True
            if message.chat.type == 'private':  # Отправлен в личку
                return 4  # Admin (only Private)
            return 3  # Admin
        else:
            if message.chat.type == 'private':
                return 2  # User (only Private)
            return 1  # User


async def scheduler():
    if Apps().current_date('%d.%m') == '31.12':
        aioschedule.every().day.at('00:00').do(new_year_msk_function)

    aioschedule.every().day.at('00:15').do(clean_disk)
    aioschedule.every().day.at('00:30').do(temp_clean)
    # 00:45 project update - Cron
    # 01:00 server restart - Cron
    aioschedule.every().day.at('19:52').do(clean_disk)
    aioschedule.every().day.at('19:5').do(clean_disk)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())


@bot.message_handler(commands=['start'])
async def start_message(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if get_status(message) in [2, 4]:  # User, Admin (only Private)
        await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        await bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}!')


@bot.message_handler(commands=['admin'])
async def get_admin_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if get_status(message) == 4:  # Admin (only Private)
        await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        await bot.send_message(message.chat.id, f'{message.from_user.first_name}, вот список доступных Вам команд:\n'
                                                f'/send_text - Отправить текстовое сообщение в группу.\n'
                                                f'/send_voice - Отправить аудио сообщение в группу.\n'
                                                f'/get_vpn - Получить сертификаты IKEv2 для доступа к VPN.\n'
                                                f'/get_kino_pub - Получить IPA файл КиноПаба (февраль 2022 г.).')


@bot.message_handler(commands=['balance'])
async def get_balance_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    mes_dict = {
        0: f'{message.from_user.first_name}, Вы в чёрном списке и Вам не доступны основные функции бота.',
        1: f'{message.from_user.first_name}, у Вас нет баланса, т.к. вы ещё не отправляли аудио сообщения.',
        2: f'{message.from_user.first_name}, у Вас осталось {get_cell(message, "get_balance")} секунд.',
        8: f'Хозяин, {message.from_user.first_name}, Вы админ бота, Вам можно всё.',
    }
    await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    if get_status(message) == 0:  # Blocked
        await bot.send_message(message.chat.id, mes_dict[0])
    if get_status(message) in [1, 2]:  # User
        if get_cell(message, 'get_balance') is None:
            await bot.send_message(message.chat.id, mes_dict[1])
        else:
            await bot.send_message(message.chat.id, mes_dict[2])
    if get_status(message) in [3, 4]:  # Admin
        await bot.send_message(message.chat.id, mes_dict[8])


@bot.message_handler(commands=['send_text'])  # Отправка текстовых сообщений в определённый чат
async def send_text_to_group(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    await bot.send_message(message.chat.id, 'Временно выключен.')
    # if get_status(message) == 4:  # Admin (only Private)
    #     Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, 'Введите id группы и текст через пробел (пример: -12345 Текст)')
    #     Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, get_groups())
    #     bot.register_next_step_handler(message, send_text_message)


def send_text_message(message):
    group_id = str(message.text).split(' ')[0]
    group_text = ' '.join(str(message.text).split(' ')[1:])
    Apps().send_chat_action(bot, chat_id=group_id, text=group_text)  # Уведомление Chat_Action
    bot.send_message(group_id, group_text)


@bot.message_handler(commands=['send_voice'])  # Отправка аудио сообщений в определённый чат
async def send_audio_to_group(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    await bot.send_message(message.chat.id, 'Временно выключен.')
    # if get_status(message) == 4:  # Admin (only Private)
    #     Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, 'Введите id группы и текст через пробел (пример: -12345 Текст)')
    #     Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, get_groups())
    #     bot.register_next_step_handler(message, send_audio_message)


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
async def disk_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if get_status(message) in [2, 4]:  # User, Admin (only Private)
        zip_folder = f'temp/temp_disk_{message.from_user.id}'
        zip_name = f"{Apps().current_date('%Y%m%d%H%M')}-{str(PassGen().pass_gen(length=6, method=['digits']))}"
        zip_password = PassGen().pass_gen(length=25, method=['lowercase', 'uppercase', 'digits'])
        zip_archive = ZipArchiver(folder=zip_folder, name=zip_name, password=zip_password).move_to_archive()
        if zip_archive is False:
            await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            await bot.send_message(message.chat.id, 'Файлы не обнаружены')
        else:
            await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            mes1 = await bot.send_message(message.chat.id, f'Архив создан.')
            if YandexDisk(YA_DISK_TOKEN).upload_file(zip_folder, zip_name) is True:
                await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
                mes2 = await bot.send_message(message.chat.id, f'Архив выгружен в Облако.')
                if YandexDisk(YA_DISK_TOKEN).publish_file(zip_name) is True:
                    await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
                    mes3 = await bot.send_message(message.chat.id, f'К архиву открыт доступ.')

                    zip_link = YandexDisk(YA_DISK_TOKEN).get_public_link(zip_name)
                    with open(f'{zip_folder}/{zip_name}.txt', 'w') as f:
                        f.write(f'Files:\n')
                        for file in os.listdir(zip_folder):
                            if file.startswith(zip_name):
                                pass
                            else:
                                os.remove(f'{zip_folder}/{file}')
                                f.write(f'{str(file)}\n')
                        f.write('\nLink available for 10 days')
                        f.write(f'\n{zip_link}')
                        f.write(f'\nZip pass - {str(zip_password)}\n\n')

                    await asyncio.sleep(5)
                    os.remove(f'{zip_folder}/{zip_name}.zip')

                    if get_cell(message, 'is_admin') is True:
                        disk_insert(message, file_name=f'{zip_name}',
                                    file_link=zip_link, file_password=zip_password,
                                    delete_days=10)
                    else:
                        disk_insert(message, file_name=f'{zip_name}',
                                    file_link=zip_link, file_password=zip_password,
                                    delete_days=5)

                    await Apps().send_chat_action(bot, chat_id=message.chat.id, action='upload_document',
                                                  sec=2)  # Уведомление Chat_Action
                    doc = await bot.send_document(message.chat.id, open(f'{zip_folder}/{zip_name}.txt', 'rb'))
                    await asyncio.sleep(5)
                    os.remove(f'{zip_folder}/{zip_name}.txt')
                    mes4 = await bot.send_message(message.chat.id, 'У Вас есть 5 минут на скачивание txt файла')
                    await bot.delete_message(message.chat.id, mes1.message_id)
                    # bot.delete_message(message.chat.id, mes2.message_id)
                    await bot.delete_message(message.chat.id, mes3.message_id)
                    await asyncio.sleep(60 * 4)
                    await bot.delete_message(message.chat.id, mes4.message_id)
                    mes5 = await bot.send_message(message.chat.id, 'Осталась 1 минута')
                    await asyncio.sleep(60)
                    await bot.delete_message(message.chat.id, mes5.message_id)
                    await bot.delete_message(message.chat.id, doc.message_id)


@bot.message_handler(commands=['get_vpn'])  # VPN
async def get_vpn_command(message):
    region_dict = {'fb-us': 'USA', 'fb-fin': 'Finland', 'fb-ru': 'Mother-Russia', 'fb-sin': 'Singapore'}
    platform_dict = {'iOS/Mac': 'mobileconfig', 'Android': 'sswan', 'Windows': 'p12'}

    if get_status(message) in [2, 4]:  # User, Admin (only Private)
        if is_vpn_user_exist(message) is False:
            vpn_insert(message, host='fb-fin')
            await Apps().send_notification(bot, message, chat_id=MY_ID, action='new_vpn_user')
        if get_cell(message, 'is_vpn_blocked') is False:
            setup = get_cell(message, 'get_vpn_setup')
            region = setup.split(' | ')[0].split(', ')
            platform = setup.split(' | ')[1].split(', ')

            await Apps().send_chat_action(bot, chat_id=message.chat.id, sec=2)  # Уведомление Chat_Action
            region_str = ''
            for r in region:
                if region_str == '':
                    region_str = region_dict[r]
                else:
                    region_str = f'{region_str}, {region_dict[r]}'
            platform_str = ''
            for p in platform:
                if platform_str == '':
                    platform_str = p
                else:
                    platform_str = f'{platform_str}, {p}'

            mes1 = await bot.send_message(message.chat.id,
                                          f'{message.from_user.first_name}, Вам доступны следующие сервера:\n '
                                          f'{region_str}\n\n и следующие OS:\n{platform_str}\n\n'
                                          f'Сертификаты собираются и через некоторое время будут Вам отправлены (до 5 минут).')

            Apps().make_folder('temp/')
            temp_path = f'temp/temp_vpn_{message.from_user.id}'
            Apps().make_folder(temp_path)

            for r in region:
                VPN(server_host=r, remote_dir=SERVER_DIR, local_dir=temp_path). \
                    add_vpn_user(get_cell(message, 'get_vpn_login'))
                VPN(server_host=r, remote_dir=SERVER_DIR, local_dir=temp_path). \
                    copy_sert(get_cell(message, 'get_vpn_login'))
                VPN(server_host=r, remote_dir=SERVER_DIR, local_dir=temp_path). \
                    delete_sert_files(get_cell(message, 'get_vpn_login'))

            await bot.delete_message(message.chat.id, mes1.message_id)

            with open('data/vpn_files/Fun.jpg', 'rb') as image:
                await Apps().send_chat_action(bot, chat_id=message.chat.id,
                                              action='upload_photo', sec=2)  # Уведомление Chat_Action
                img = await bot.send_photo(message.chat.id, image)
            with open('data/vpn_files/ReadMe.md', 'rb') as manual:
                await Apps().send_chat_action(bot, chat_id=message.chat.id,
                                              action='upload_document', sec=2)  # Уведомление Chat_Action
                mes2 = await bot.send_document(message.chat.id, manual, disable_notification=True)
            # with open('data/vpn_files/Manual iOS.mov', 'rb') as manual:  # Много весит, не отправляется
            #     await Apps().send_chat_action(bot, chat_id=message.chat.id,
            #                                   action='upload_video', sec=2)  # Уведомление Chat_Action
            #     vid = await bot.send_document(message.chat.id, manual, disable_notification=True)
            mes_id_list = []
            for file in os.listdir(temp_path):
                for p in platform:
                    if platform_dict[p] == file.split('.')[1]:
                        with open(f'{temp_path}/{file}', 'rb') as certificate:
                            await Apps().send_chat_action(bot, chat_id=message.chat.id,
                                                          action='upload_document', sec=2)  # Уведомление Chat_Action
                            mes = await bot.send_document(message.chat.id, certificate, disable_notification=True)
                            mes_id_list.append(mes.message_id)
            for p in platform:
                if p == 'Windows':
                    for r in region:
                        with open(f'data/vpn_files/ikev2_config_import_{r.split("fb-")[1]}.cmd', 'rb') as manual:
                            await Apps().send_chat_action(bot, chat_id=message.chat.id,
                                                          action='upload_document', sec=2)  # Уведомление Chat_Action
                            mes3 = await bot.send_document(message.chat.id, manual, disable_notification=True)
                            mes_id_list.append(mes3.message_id)

            delete_time = 5
            mes4 = await bot.send_message(message.chat.id, f'У Вас {delete_time} минуты на скачивание.')

            await asyncio.sleep(delete_time * 60)
            for inf_mes in mes_id_list:
                await asyncio.sleep(1)
                await bot.delete_message(message.chat.id, inf_mes)
            await bot.delete_message(message.chat.id, mes2.message_id)
            await bot.delete_message(message.chat.id, mes4.message_id)
            await bot.delete_message(message.chat.id, img.message_id)
            # await bot.delete_message(message.chat.id, vid.message_id)


@bot.message_handler(commands=['get_kino_pub'])  # получить файл КиноПаба (IPA)
async def kino_pub_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if get_status(message) == 4:  # Admin (only Private)
        with open('data/kuno_pub/cncrt.ipa', 'rb') as certificate:
            await Apps().send_chat_action(bot, chat_id=message.chat.id,
                                          action='upload_document', sec=2)  # Уведомление Chat_Action
            kp_file = await bot.send_document(message.chat.id, certificate, disable_notification=True)
            await asyncio.sleep(2 * 60)
            await bot.delete_message(message.chat.id, kp_file.message_id)


@bot.message_handler(commands=['currency'])  # Курс Валют
async def currency_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if get_status(message) != 0:  # Not Blocked
        await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        await bot.send_message(message.chat.id,
                               f'Текущий курс валют:\n$ - {currency("USD")} ₽\n€ - {currency("EUR")} ₽')


@bot.message_handler(commands=['id'])  # Отправка id пользователя и группы (если бот в группе)
async def id_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if get_status(message) != 0:  # Not Blocked
        user_id = str(message.from_user.id)
        group_id = str(message.chat.id)
        await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
        if user_id == group_id:
            await bot.send_message(message.chat.id, f'Ваш ID: {user_id}')
        else:
            await bot.send_message(message.chat.id, f'Ваш ID: {user_id}\nID группы: {group_id}')


@bot.message_handler(commands=['translate'])  # Переводчик
async def translate_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    await bot.send_message(message.chat.id, 'Временно выключен.')
    # if get_status(message) in [2, 4]:  # User, Admin (only Private)
    #     Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, MainStrings().button_translator)
    #     bot.register_next_step_handler(message, translate)


def translate(message):
    temp_path = 'temp/'
    Apps().make_folder(temp_path)  # Создать папку если она отсутствует
    iam_file = temp_path + 'iam.txt'
    Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    while True:
        try:
            iam_file = temp_path + 'iam.txt'
            if IAM_token(OAUTH_TOKEN).file_exist(iam_file) is False:
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
async def weather_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    await bot.send_message(message.chat.id, 'Временно выключен.')
    # if get_status(message) in [2, 4]:  # User, Admin (only Private)
    #     Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, MainStrings().button_weather)
    #     bot.register_next_step_handler(message, weather)


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
async def transliterate_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    await bot.send_message(message.chat.id, 'Временно выключен.')
    # if get_status(message) in [2, 4]:  # User, Admin (only Private)
    #     Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, MainStrings().button_transliterate)
    #     bot.register_next_step_handler(message, transliterate_hieroglyphs)


def transliterate_hieroglyphs(message):
    Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    result = Transliterate.transliterate_hieroglyphs(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['passport'])  # Транслитерация имени и фамилии для загранпаспорта
async def transliterate_command(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    await bot.send_message(message.chat.id, 'Временно выключен.')
    # if get_status(message) in [2, 4]:  # User, Admin (only Private)
    #     Apps().send_chat_action(bot, chat_id=message.chat.id, sec=3)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, MainStrings().passport)
    #     Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
    #     bot.send_message(message.chat.id, MainStrings().button_passport)
    #     bot.register_next_step_handler(message, transliterate_passport)


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
async def handler_content_types(message):
    work_with_db(message)  # Основная функция которая делает записи в DB
    if message.content_type == 'voice' and get_cell(message,
                                                    'is_blocked') is False and message.from_user.is_bot is False:
        if get_cell(message, 'is_admin') is True:
            await work_with_audio(message)
        else:
            if (get_total_audio(message)) <= 0:
                await Apps().send_notification(bot, message, chat_id=MY_ID, action='no_time')
                await bot.send_message(message.chat.id, MainStrings().no_time)
            elif message.voice.duration >= 30:
                await bot.send_message(message.chat.id, MainStrings().max_length)
            else:
                audio_time = get_total_audio(message) - message.voice.duration
                update_total_audio(message, audio_time)
                await work_with_audio(message)

    elif message.from_user.is_bot is False and message.chat.type != 'private':
        if message.content_type == 'new_chat_members':  # Реагирует на уведомление "присоединился к нам"
            if message.json['new_chat_members'][0]['is_bot'] is False:
                update_is_left(message, False)
                await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
                await bot.send_message(message.chat.id, f'Добро пожаловать {message.new_chat_members[0].first_name}')
        elif message.content_type == 'left_chat_member':  # Реагирует на уведомление "покинул группу"
            if message.json['left_chat_member']['is_bot'] is False:
                update_is_left(message, True)
                await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
                await bot.send_message(message.chat.id, f'До встречи {message.left_chat_member.first_name}.')
        elif message.content_type == 'new_chat_title':
            await Apps().echo_voice(bot, message, 'title')  # Отправляет случайное сообщение из title.txt
        elif message.content_type == 'new_chat_photo':
            await Apps().echo_voice(bot, message, 'avatar')  # Отправляет случайное сообщение из avatar.txt
        elif message.content_type == 'text':
            log_insert(message)  # Запись логов в DB
            if message.reply_to_message is not None and message.reply_to_message.from_user.id == int(
                    TOKEN.split(':')[0]):
                await Apps().send_notification(bot, message, chat_id=MY_ID, action='reply_message')

    elif message.from_user.is_bot is False and message.chat.type == 'private':
        if message.content_type == 'document':
            Apps().make_folder('temp/')
            temp_path = f'temp/temp_disk_{message.from_user.id}'
            Apps().make_folder(temp_path)

            file_name = f'{temp_path}/{message.document.file_name}'
            await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            if (message.document.file_size / 1000000) < 21:
                file_info = await bot.get_file(message.document.file_id)
                file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
                with open(file_name, 'wb') as f:
                    f.write(file.content)
                await bot.send_message(message.chat.id, f'Файл "{message.document.file_name}" выгружен.')
                await asyncio.sleep(5)
                await bot.delete_message(message.chat.id, message.message_id)
            else:
                await bot.send_message(message.chat.id,
                                       f'ОШИБКА API "{message.document.file_name}" > 20mb')
        elif message.content_type == 'sticker' and get_cell(message, 'is_blocked') is False:
            await Apps().send_chat_action(bot, chat_id=message.chat.id)  # Уведомление Chat_Action
            await bot.send_message(message.chat.id, f'ID стикера: {message.sticker.file_id}')
        elif message.content_type == 'location' and get_cell(message, 'is_blocked') is False:
            await Apps().send_chat_action(bot, chat_id=message.chat.id, sec=2)  # Уведомление Chat_Action
            await bot.send_message(message.chat.id, f'lat = {message.location.latitude}\n'
                                                    f'lon = {message.location.longitude}\n'
                                                    f'[{message.location.latitude}, {message.location.longitude}]')


async def work_with_audio(message):
    temp_path = 'temp/'
    Apps().make_folder(temp_path)  # Создать папку если она отсутствует
    iam_file = f'{temp_path}/iam.txt'
    speech_file = f'{temp_path}/{message.voice.file_id}.ogg'
    file_info = await bot.get_file(message.voice.file_id)
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
    await Apps().send_chat_action(bot, chat_id=message.chat.id, text=text)  # Уведомление Chat_Action
    if len(text) == 0:
        await bot.send_message(message.chat.id, MainStrings().no_words)
    else:
        await bot.send_message(message.chat.id, f'{message.from_user.first_name}:\n{text}')
        await Apps().echo_voice(bot, message, 'voice')  # Отправляет случайное сообщение из voice.txt
    await asyncio.sleep(5)
    os.remove(speech_file)  # Удаляет аудио файл после его преобразования и отправки как текстового сообщения


if __name__ == '__main__':
    asyncio.run(main())
