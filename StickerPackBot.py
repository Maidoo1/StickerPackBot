import os
import telebot

tb_token = '409810310:AAGVGBAk9n4iojkMO61-l_em7YlT4zG_8Rk'

bot = telebot.TeleBot(tb_token)
url = 'https://web.telegram.org/#/im?p=@Stickers'


class Sticker:
    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def upload_sticker(message):
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = file_info.file_path[:-4] + 'png'

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        return src

    def create_sticker_pack(self, pack_name, pack_title, message):
        with open(self.upload_sticker(message), 'rb') as send_file:
            bot.create_new_sticker_set(self.user_id, pack_name, pack_title,
                                   send_file, message.sticker.emoji)

            bot.send_message(message.chat.id, 't.me/addstickers/' + pack_name)



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!\n'
                                      'Send me stickers and I\'ll convert it in png and send you sticker\'s emoji.\n'
                                      'After that you can do sticker packs with your loved stickers.\n'
                                      'Just create new pack in @Stickers bot and forward this png and emoji!\n')


@bot.message_handler(content_types=['sticker'])
def create_pack(message):
    print(message)
    asd = Sticker(message.from_user.id)
    asd.create_sticker_pack('Ananmsdda_by_stickerpackbot', '131adadaqqqqsd', message)

    # os.remove(src)

    
if __name__ == '__main__':
    bot.polling(none_stop=True)