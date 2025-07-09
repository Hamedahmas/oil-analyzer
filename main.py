import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

# 🛡 تنظیمات ربات تلگرام
TELEGRAM_TOKEN = "7754260268:AAE2JjAal8Di-qOTOUf0lBRN4FNNl3VrUo4"
TELEGRAM_CHAT_ID = "-1002233437580"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("خطا در ارسال به تلگرام:", e)

def fetch_oil_headlines():
    url = "https://oilprice.com/Latest-Energy-News/World-News/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = []
        for div in soup.find_all("div", class_="headline_row"):
            title_span = div.find("span", class_="article_name")
            link_tag = div.find("a", class_="full_parent")
            if title_span and link_tag:
                title = title_span.get_text(strip=True)
                link = link_tag["href"]
                headlines.append((title, link))
        return headlines
    except Exception as e:
        print("خطا در دریافت اخبار:", e)
        return []

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "مثبت ✅"
    elif polarity < -0.1:
        return "منفی ❌"
    else:
        return "خنثی ⚪️"

def main():
    headlines = fetch_oil_headlines()
    if not headlines:
        send_telegram_message("⛔️ هیچ خبری برای تحلیل پیدا نشد.")
        return

    message = f"🛢 تحلیل سریع بازار نفت\n\nتعداد تیتر بررسی‌شده: {len(headlines)}\n"
    sentiment_score = 0

    for title, link in headlines[:5]:
        sentiment = analyze_sentiment(title)
        message += f"\n📰 {title}\n🔗 {link}\n📊 احساس: {sentiment}\n"
        if sentiment == "مثبت ✅":
            sentiment_score += 1
        elif sentiment == "منفی ❌":
            sentiment_score -= 1

    message += f"\n📊 امتیاز سنتیمنت: {sentiment_score}\n\n📡 سیستم تحلیل اتوماتیک | بروزرسانی هر 30 دقیقه"
    send_telegram_message(message)

if __name__ == "__main__":
    main()
