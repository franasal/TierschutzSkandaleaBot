import requests
import streamlit as st

# Get token and chat ID from Streamlit secrets or fallback placeholders
TELEGRAM_BOT_TOKEN = st.secrets.get("telegram_bot_token", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = st.secrets.get("telegram_chat_id", "YOUR_TELEGRAM_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

API_URL = 'https://tierschutz-skandale.de/wp-json/wp/v2/posts?_embed'

def get_posts(per_page=5):
    url = f"https://tierschutz-skandale.de/wp-json/wp/v2/posts?_embed&per_page={per_page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Failed to fetch posts: {e}")
        return []

def send_telegram_message(text, chat_id):
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

st.title("Tierschutz Skandale Bot")

st.header("Latest Posts")
posts = get_posts()

for post in posts:
    title = post.get('title', {}).get('rendered', 'No title')
    link = post.get('link', 'No link')
    st.markdown(f"**{title}**  \n{link}")

st.header("Send Telegram Message")

message = st.text_area("Message to send")

if st.button("Send Message"):
    if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "YOUR_TELEGRAM_CHAT_ID":
        st.error("Telegram chat ID is missing or not set in secrets.")
    elif not message:
        st.error("Please enter a message.")
    else:
        success, result = send_telegram_message(message, TELEGRAM_CHAT_ID)
        if success:
            st.success("Message sent successfully!")
        else:
            st.error(f"Failed to send message: {result}")
