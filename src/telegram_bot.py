import json
import requests

def send_telegram_message(message):
    config = json.load(open("config/settings.json"))
    token = config["telegram_token"]
    chat_id = config["telegram_chat_id"]
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)
