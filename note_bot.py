import os

from telegram.ext import Updater, CommandHandler, Filters
from telegram.ext import CallbackQueryHandler, CallbackContext, MessageHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


class Bot:

    def __init__(self, token):

        updater = Updater(token, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler('s', self.start))

        dp.add_handler(CallbackQueryHandler(self.main_menu, pattern='main'))
        dp.add_handler(CallbackQueryHandler(self.second_menu, pattern='m1'))
        dp.add_handler(CallbackQueryHandler(self.log, pattern='log'))

        # on non command i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(
            Filters.text & ~Filters.command,
            self.echo
            ))

        print('bot has started')

        updater.start_polling()

        updater.idle()

    def echo(self, update: Update, context: CallbackContext) -> None:
        """Echo the user message."""
        update.message.reply_text(update.message.text)

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

    def second_menu_keyboard(self):
        keyboard = [
            [InlineKeyboardButton(
                'Vacuuming the Floor',
                callback_data='Vacuuming the Floor'
            )],
            [InlineKeyboardButton(
                'Wiping the Tables',
                callback_data='log Wiping the Tables'
            )],
            [InlineKeyboardButton(
                'Chair Cleaning',
                callback_data='log Chair Cleaning'
            )],
            [InlineKeyboardButton(
                'Extractor Fan Cleaning',
                callback_data='log Extractor Fan Cleaning'
            )],
            [InlineKeyboardButton(
                'Cooker',
                callback_data='log Cooker'
            )],
            [InlineKeyboardButton(
                'Dishwasher Cleaning',
                callback_data='log Dishwasher Cleaning'
            )]
        ]
        return InlineKeyboardMarkup(keyboard)

    def log(self, update: Update, context: CallbackContext):
        print(update.callback_query.data)


if __name__ == '__main__':
    bot = Bot(token=os.environ['NOTE_BOT_TOKEN'])
