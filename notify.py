import os
from telegram import Bot
from main import send_new_posts

bot = Bot(token=os.environ['TELEGRAM_TOKEN'])
send_new_posts(bot)
