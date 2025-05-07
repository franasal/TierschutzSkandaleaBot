import json
import random
import requests
from telegram import Bot
from telegram.ext import CommandHandler, Updater

# === CONFIG ===
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_URL = 'https://tierschutz-skandale.de/wp-json/wp/v2/posts?_embed'
CACHE_FILE = 'latest_post.json'

# === FUNKTIONEN ===

def get_posts(per_page=5, page=1):
    url = f'{API_URL}&per_page={per_page}&page={page}'
    res = requests.get(url)

    try:
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {res.status_code} – {res.text}")
        raise
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Error: {res.text}")
        raise

def get_latest_post_id():
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f).get("last_id", 0)
    except FileNotFoundError:
        return 0

def save_latest_post_id(post_id):
    with open(CACHE_FILE, 'w') as f:
        json.dump({"last_id": post_id}, f)

def send_new_posts(bot):
    posts = get_posts(per_page=5)
    if not posts:
        return

    last_id = get_latest_post_id()
    newest_post_id = posts[0]['id']

    if last_id == 0:
        # Erstlauf: Nur speichern, nichts senden
        save_latest_post_id(newest_post_id)
        print("Erstlauf: Nur ID gespeichert.")
        return

    new_posts = [p for p in posts if p['id'] > last_id]

    if new_posts:
        for post in reversed(new_posts):
            msg = f"*{post['title']['rendered']}*\n{post['link']}"
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
        save_latest_post_id(new_posts[0]['id'])

def random_post(update, context):
    page = random.randint(1, 20)
    posts = get_posts(per_page=1, page=page)
    if posts:
        post = posts[0]
        msg = f"*{post['title']['rendered']}*\n{post['link']}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Kein Beitrag gefunden.")

# === BOT SETUP ===

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("zufall", random_post))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
