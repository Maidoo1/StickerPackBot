import os
import telebot

tb_token = '409810310:AAGVGBAk9n4iojkMO61-l_em7YlT4zG_8Rk'

bot = telebot.TeleBot(tb_token)
url = 'https://web.telegram.org/#/im?p=@Stickers'


class Stickers:
    def __init__(self, user_id):
        self.user_id = user_id
        self.stickers = []
        self.pack_name = 'None'
        self.src = 'None'
        self.max_pack = 120

    def upload_sticker(self, message):
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        self.src = file_info.file_path[:-4] + 'png'

        with open(self.src, 'wb') as new_file:
            new_file.write(downloaded_file)

    def is_upload(self):
        return True if self.src in self.stickers else False

    def create_sticker_pack(self, message):
        self.upload_sticker(message)
        self.stickers.append(self.src)
        with open(self.src, 'rb') as send_file:
            bot.create_new_sticker_set(self.user_id, self.pack_name + '_by_stickerpackbot',
                                       self.pack_name, send_file, message.sticker.emoji)

        bot.send_message(message.chat.id, 'Sticker #' + str(len(self.stickers)) + ' has been added\n'
                         'You can add only ' + str(self.max_pack - len(self.stickers)) + ' stickers')

    def add_sticker_to_pack(self, message):
        self.upload_sticker(message)
        if not self.is_upload():
            self.stickers.append(self.src)
            with open(self.src, 'rb') as send_file:
                bot.add_sticker_to_set(message.from_user.id, self.pack_name + '_by_stickerpackbot',
                                       send_file, message.sticker.emoji, None)

            bot.send_message(message.chat.id, 'Sticker #' + str(len(self.stickers)) + ' has been added\n'
                             'You can add only ' + str(self.max_pack - len(self.stickers)) + ' stickers')
        else:
            return bot.send_message(message.chat.id, 'This sticker is in pack already!')

    def clean_folder(self):
        [os.remove(i) for i in self.stickers]


user_dict = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!\n'
                                      '/pack_from_stickers - create pack from stickers')


@bot.message_handler(commands=['pack_from_stickers'])
def pack_from_stickers_name(message):
    user_dict[message.chat.id] = Stickers(message.chat.id)

    request = bot.send_message(message.chat.id, 'Pass the sticker pack name')
    bot.register_next_step_handler(request, sticker_pack_name)


def sticker_pack_name(message):
    user_dict[message.chat.id].pack_name = str(message.text)

    request = bot.send_message(message.chat.id, 'Send sticker')
    bot.register_next_step_handler(request, create_pack)


@bot.message_handler(content_types=['text, sticker'])
def create_pack(message):
    user_dict[message.chat.id].create_sticker_pack(message)

    request = bot.send_message(message.chat.id, 'Send next sticker\n'
                                                'Or pass /stop to finish your sticker pack')
    bot.register_next_step_handler(request, add_sticker)


def add_sticker(message):
    if str(message.text) == '/stop':
        user_dict[message.chat.id].clean_folder()
        return bot.send_message(message.chat.id, 't.me/addstickers/' + user_dict[message.chat.id].pack_name
                                + '_by_stickerpackbot')

    user_dict[message.chat.id].add_sticker_to_pack(message)
    request = bot.send_message(message.chat.id, 'Send next sticker\n'
                                                'Or pass /stop to finish your sticker pack')
    bot.register_next_step_handler(request, add_sticker)


if __name__ == '__main__':
    bot.polling(none_stop=True)