import streamlit as st import requests

Telegram bot token and API URL

TELEGRAM_BOT_TOKEN = st.secrets.get("telegram_bot_token", "YOUR_TELEGRAM_BOT_TOKEN") BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

st.title("Tierschutz-Skandale Telegram Bot Control")

Session state for storing last update_id to avoid repeats

if "last_update_id" not in st.session_state: st.session_state.last_update_id = 0

Fetch latest messages

def fetch_messages(): url = f"{BASE_URL}/getUpdates?offset={st.session_state.last_update_id + 1}" res = requests.get(url) if res.status_code != 200: st.error("Failed to fetch updates") return [] data = res.json() messages = [] for result in data.get("result", []): update_id = result["update_id"] message = result.get("message") if message: chat_id = message["chat"]["id"] text = message.get("text", "") username = message["chat"].get("username", "unknown") messages.append({ "update_id": update_id, "chat_id": chat_id, "username": username, "text": text, }) st.session_state.last_update_id = update_id return messages

Reply to a Telegram user

def send_reply(chat_id, text): url = f"{BASE_URL}/sendMessage" payload = {"chat_id": chat_id, "text": text} res = requests.post(url, json=payload) return res.ok

st.subheader("Fetch new Telegram messages") if st.button("Fetch Messages"): new_messages = fetch_messages() if not new_messages: st.info("No new messages.") else: for i, msg in enumerate(new_messages): st.write(f"{msg['username']}: {msg['text']}") reply = st.text_input(f"Reply to {msg['username']}", key=f"reply_{i}") if st.button(f"Send Reply {i}"): if send_reply(msg["chat_id"], reply): st.success("Reply sent.") else: st.error("Failed to send reply.")
