import os
import time
import random
import datetime


class Apps:
    def __init__(self):
        self.data_path = 'data'

    def current_date(self, time_format='%Y-%m-%d %H:%M:%S'):  # Текущее время и дата по Москве (Часовой пояс +3)
        offset = datetime.timezone(datetime.timedelta(hours=3))
        date = datetime.datetime.now(offset).strftime(time_format)  # time_format('%Y-%m-%d %H:%M:%S')
        return date

    def make_folder(self, directory):  # Создать папку если она отсутствует в рабочей папке
        try:
            os.stat(directory)
        except OSError:
            os.mkdir(directory)

    async def send_chat_action(self, bot, chat_id, action='typing', sec=1, text=None):  # Уведомление Chat_Action
        await bot.send_chat_action(chat_id, action)
        # action typing/choose_sticker/record_audio/upload_document/upload_photo
        if text is not None:
            if len(text) < 15:
                sec = 1
            elif 15 <= len(text) < 25:
                sec = 2
            elif 25 <= len(text) < 35:
                sec = 3
            elif 35 <= len(text) < 45:
                sec = 4
            elif len(text) >= 45:
                sec = 5
            elif len(text) >= 100:
                sec = 5
        time.sleep(sec)

    async def send_notification(self, bot, message, chat_id, action):
        # type = reply_message/new_user/new_group/no_time/...
        user_id = str(message.from_user.id)
        username = str(message.from_user.username)
        try:
            full_name = str(f'{message.from_user.first_name} {message.from_user.last_name}')
        except TypeError:
            full_name = str(message.from_user.first_name)
        group_id = str(message.chat.id)[1:]
        group_title = str(message.chat.title)
        message_id = str(message.message_id)
        text = str(message.text)
        if action == 'reply_message':
            await bot.send_message(chat_id, f'Новое reply сообщение:\n'
                                            f'id {group_id} - "{group_title}")\n'
                                            f'id {user_id} - {full_name} ({username})\n'
                                            f'message_id {message_id} - {text}')
        elif action == 'new_user':
            await bot.send_message(chat_id, f'Новый пользователь:\nid {user_id} - {full_name} ({username})')
        elif action == 'new_group':
            await bot.send_message(chat_id, f'Новая группа:\nid {group_id} - "{group_title}")')
        elif action == 'no_time':
            await bot.send_message(chat_id, f'У пользователя кончилось время:\nid {user_id} - {full_name} ({username})')
        elif action == 'new_vpn_user':
            await bot.send_message(chat_id,
                                   f'Появился новый пользователь VPN:\nid {user_id} - {full_name} ({username})')

    async def echo_voice(self, bot, message, txt_file,
                         percent=25):  # Отправляет случайное сообщение из answers_NAME.txt
        answer_file = f'{self.data_path}/{txt_file}.txt'
        number = int(100 / percent)
        random_number = random.randint(1, number)
        if random_number == 1:
            with open(answer_file, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                phrase = random.choice(lines)
                await Apps().send_chat_action(bot, chat_id=message.chat.id, text=phrase)  # Уведомление Chat_Action
                bot.send_message(message.chat.id, phrase)
                print(phrase)
