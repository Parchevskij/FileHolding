import requests
import os
from telebot import TeleBot
import numpy as np

TOKEN = '1729656253:AAFL09iQJ71DTiR9uXPSJjB_b-3ONps_clk'
bot = TeleBot(TOKEN)

user_id = list()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Welcome, {message.from_user.first_name}')
    user_id.append(message.from_user.id)

    with open('users_data/users_id.txt', 'w') as f:
        unique_users = np.unique(user_id).tolist()

        for i in unique_users:
            print('here is {}'.format(i))
            f.write(str(i)+'\n')


@bot.message_handler(content_types=['document'])
def file_downloader(message):
    filename = message.document.file_name
    file_id = message.document.file_id
    file_id_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_id_info.file_path)

    with open('database/'+filename, 'wb') as f:
        f.write(downloaded_file)

    method = "sendMessage"
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    bot_message = 'Database was updated: \n' + 'File {} was added'.format(filename)

    with open('users_data/users_id.txt', 'r') as f:
        users_id = f.readlines()

        for id in users_id:
            data = {"chat_id": id,
                    "text": bot_message}
            requests.post(url, data=data)


bot.polling(none_stop=True)
