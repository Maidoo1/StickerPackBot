import os
import telebot

tb_token = '409810310:AAGVGBAk9n4iojkMO61-l_em7YlT4zG_8Rk'

bot = telebot.TeleBot(tb_token)
url = 'https://web.telegram.org/#/im?p=@Stickers'


class Sticker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.pack_name = 'None'
        self.pack_title = 'None'

    @staticmethod
    def upload_sticker(message):
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = file_info.file_path[:-4] + 'png'

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        return src

    def create_sticker_pack(self, message):
        src = self.upload_sticker(message)
        self.pack_name = self.pack_name + '_by_stickerpackbot'

        with open(src, 'rb') as send_file:
            bot.create_new_sticker_set(self.user_id, self.pack_name,
                                       self.pack_title, send_file, message.sticker.emoji)

        # os.remove(src)

    def add_sticker_to_pack(self, message):
        src = self.upload_sticker(message)

        with open(src, 'rb') as send_file:
            bot.add_sticker_to_set(message.from_user.id, self.pack_name, send_file, message.sticker.emoji, None)


user_dict = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!\n'
                                      'Send me stickers and I\'ll convert it in png and send you sticker\'s emoji.\n'
                                      'After that you can do sticker packs with your loved stickers.\n'
                                      'Just create new pack in @Stickers bot and forward this png and emoji!\n'
                                      '/pack_from_stickers - create pack from stickers')


@bot.message_handler(commands=['pack_from_stickers'])
def pack_from_stickers_name(message):
    user_dict[message.chat.id] = Sticker(message.chat.id)

    request = bot.send_message(message.chat.id, 'Pass the sticker pack name')
    bot.register_next_step_handler(request, sticker_pack_name)


def sticker_pack_name(message):
    user_dict[message.chat.id].pack_name = str(message.text)

    request = bot.send_message(message.chat.id, 'Pass the sticker pack title')
    bot.register_next_step_handler(request, sticker_pack_title)


def sticker_pack_title(message):
    user_dict[message.chat.id].pack_title = str(message.text)

    request = bot.send_message(message.chat.id, 'Send 1 sticker')
    bot.register_next_step_handler(request, create_pack)


@bot.message_handler(content_types=['text, sticker'])
def create_pack(message):
    user_dict[message.chat.id].create_sticker_pack(message)

    request = bot.send_message(message.chat.id, 'Send sticker')
    bot.register_next_step_handler(request, add_sticker)


def add_sticker(message):
    if str(message.text) == '/stop':
        return bot.send_message(message.chat.id, 't.me/addstickers/' + user_dict[message.chat.id].pack_name)

    user_dict[message.chat.id].add_sticker_to_pack(message)
    request = bot.send_message(message.chat.id, 'sticker has been added')
    bot.register_next_step_handler(request, add_sticker_1)


def add_sticker_1(message):
    if str(message.text) == '/stop':
        return bot.send_message(message.chat.id, 't.me/addstickers/' + user_dict[message.chat.id].pack_name)

    user_dict[message.chat.id].add_sticker_to_pack(message)
    request = bot.send_message(message.chat.id, 'Send sticker')
    bot.register_next_step_handler(request, add_sticker)


if __name__ == '__main__':
    bot.polling(none_stop=True)