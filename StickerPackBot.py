import telebot

tb_token = '409810310:AAGVGBAk9n4iojkMO61-l_em7YlT4zG_8Rk'

bot = telebot.TeleBot(tb_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!\n'
                                      'Send me your loved stickers and I\'ll do a sticker pack')


@bot.message_handler(content_types=['sticker'])
def create_pack(message):
    try:
        sticker = message.sticker.file_id
        bot.send_message(message.chat.id, sticker)
        bot.send_sticker(message.chat.id, sticker)
        # print(sticker)
    except:
        bot.send_message(message.chat.id, 'Something went wrong')

if __name__ == '__main__':
    bot.polling(none_stop=True)