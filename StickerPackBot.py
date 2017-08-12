import telebot
import os

tb_token = '409810310:AAGVGBAk9n4iojkMO61-l_em7YlT4zG_8Rk'

bot = telebot.TeleBot(tb_token)
url = 'https://web.telegram.org/#/im?p=@Stickers'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!\n'
                                      'Send me stickers and I\'ll convert it in png and send you sticker\'s emoji.\n'
                                      'After that you can do sticker packs with your loved stickers.\n'
                                      'Just create new pack in @Stickers bot and forward this png and emoji!\n')


@bot.message_handler(content_types=['sticker'])
def create_pack(message):
    file_info = bot.get_file(message.sticker.file_id)
    file_download = bot.download_file(file_info.file_path)
    src = file_info.file_path[:-4] + 'png'

    with open(src, 'wb') as new_file:
        new_file.write(file_download)

    bot.send_message(message.chat.id, 'Sticker in png:')
    with open(src, 'rb') as send_file:
        bot.send_document(message.chat.id, send_file)

    os.remove(src)

    bot.send_message(message.chat.id, 'Sticker\'s emoji:')
    bot.send_message(message.chat.id, message.sticker.emoji)


if __name__ == '__main__':
    bot.polling(none_stop=True)