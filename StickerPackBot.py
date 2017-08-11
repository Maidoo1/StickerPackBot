import telebot

tb_token = '409810310:AAGVGBAk9n4iojkMO61-l_em7YlT4zG_8Rk'

bot = telebot.TeleBot(tb_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!\n'
                                      'Send me your loved stickers and I\'ll do a sticker pack')


@bot.message_handler(content_types=['sticker'])
def create_pack(message):
    print(message)
    print(message.chat.id)
    file_info = bot.get_file(message.sticker.file_id)
    print(file_info)
    file_download = bot.download_file(file_info.file_path)
    print(file_download)
    src = file_info.file_path[:-4] + 'png'

    print(src)
    with open(src, 'wb') as new_file:
        new_file.write(file_download)

    with open(src, 'rb') as send_file:
        bot.send_document(message.chat.id, send_file)

if __name__ == '__main__':
    bot.polling(none_stop=True)