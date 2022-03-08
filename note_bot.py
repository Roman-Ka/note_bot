import os

from telegram.ext import Updater, CommandHandler, Filters
from telegram.ext import CallbackQueryHandler, CallbackContext, MessageHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


class LinkNoteHandler:

    def __init__(self, path):
        self._folder_path = os.path.abspath(path)

    def get_links(self):
        with open(os.path.join(self._folder_path, 'links.md'), 'r') as f:
            links_note = f.read()
        return links_note

    @property
    def categories(self):
        contents = self.get_links()
        # Find names of all categories from the whole doc
        proj_names = contents.split('\n## ')
        # split for the first 'word'
        proj_names = [x.split('\n')[0] for x in proj_names[1:]]
        return proj_names


class Bot:

    def __init__(self, token):
        self._note_handler = LinkNoteHandler(
            path=os.environ['PATH_TO_NOTES']
        )

        updater = Updater(token, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler('s', self.start))

        dp.add_handler(CallbackQueryHandler(self.main_menu, pattern='main'))
        dp.add_handler(CallbackQueryHandler(self.second_menu, pattern='m1'))
        dp.add_handler(CallbackQueryHandler(self.log, pattern='log'))

        # on non command i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(
            Filters.text & ~Filters.command,
            self.receive_message
            ))

        print('bot has started')

        updater.start_polling()

        updater.idle()

    def receive_message(self,
                        update: Update,
                        context: CallbackContext) -> None:
        """Echo the user message."""
        if 'http' in update.message.text:
            update.message.reply_text(
                'Link:category',
                reply_markup=self.link_categories_menu()
            )
        self.current_link = update.message.text

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Hi!',
            reply_markup=self.main_menu_keyboard()
        )

    def main_menu(self, update: Update, context: CallbackContext):
        query = update.callback_query
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=self.main_menu_message(),
            reply_markup=self.main_menu_keyboard()
        )

    def main_menu_keyboard(self):
        keyboard = [[
            InlineKeyboardButton('Log New Activity', callback_data='m1')
        ]]
        return InlineKeyboardMarkup(keyboard)

    def second_menu(self, update: Update, context: CallbackContext):
        query = update.callback_query
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Which activity?',
            reply_markup=self.second_menu_keyboard()
        )

    def link_categories_menu(self):
        keyboard = [
            [InlineKeyboardButton(
                name,
                callback_data=f'log {name}'
            )] for name in self._note_handler.categories
        ]
        keyboard.append([InlineKeyboardButton(
            '/add new/',
            callback_data='add_new')])

        return InlineKeyboardMarkup(keyboard)

    def log(self, update: Update, context: CallbackContext):
        category = update.callback_query.data.split('log ')[1]
        

        print(update.callback_query.data)


if __name__ == '__main__':
    bot = Bot(token=os.environ['NOTE_BOT_TOKEN'])
