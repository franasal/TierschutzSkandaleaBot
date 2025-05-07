import os
import requests
import telegram

# Get Telegram Token and Chat ID from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Check if token and chat_id are set
if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN or CHAT_ID is not set!")

# Telegram bot setup
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# API URL for fetching posts
API_URL = 'https://tierschutz-skandale.de/wp-json/wp/v2/posts?_embed'

# Function to fetch posts from the API
def get_posts(per_page=5, page=1):
    url = "https://tierschutz-skandale.de/wp-json/wp/v2/posts?_embed&per_page=2"
    headers = {"User-Agent": "Mozilla/5.0"}  # important for some servers

    res = requests.get(url, headers=headers)
    print(f"Status: {res.status_code}")
    print(res.text)

    try:
        res.raise_for_status()  # Will raise an error for non-200 status codes
        return res.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {res.status_code} – {res.text}")
        raise
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Error: {res.text}")
        raise

# Function to send a Telegram message
def send_telegram_message(bot, message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML", disable_web_page_preview=False)
        print("Message sent.")
    except Exception as e:
        print(f"Telegram error: {e}")

# Main function to fetch posts and send messages
def send_new_posts():
    posts = get_posts(per_page=5)

    if not posts:
        print("No posts found.")
        return

    for post in posts:
        title = post.get('title', {}).get('rendered', 'No title')
        link = post.get('link', 'No link')
        message = f"New post: <b>{title}</b>\n{link}"
        send_telegram_message(bot, message)

if __name__ == "__main__":
    send_new_posts()
