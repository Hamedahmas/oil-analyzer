import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import time

# تنظیمات ربات تلگرام (توکن و چت آیدی کانال خصوصی)
TELEGRAM_TOKEN = "7754260268:AAE2JjAal8Di-qOTOUf0lBRN4FNNl3VrUo4"
TELEGRAM_CHAT_ID = "-1002233437580"

# ارسال پیام به تلگرام
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    print("Telegram:", response.status_code)

# دریافت آخرین خبرها از oilprice
def fetch_oilprice_news():
    base_url = "https://oilprice.com"
    news_url = "https://oilprice.com/latest-energy-news/world-news/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(news_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.select(".categoryArticle")
        news_items = []

        for article in articles[:5]:
            title_tag = article.select_one("h4 a")
            if not title_tag:
                continue
            title = title_tag.text.strip()
            link = base_url + title_tag["href"]

            article_res = requests.get(link, headers=headers, timeout=10)
            article_soup = BeautifulSoup(article_res.text, "html.parser")
            paragraphs = article_soup.select(".article-content p")
            content = " ".join(p.text for p in paragraphs)

            news_items.append({
                "title": title,
                "link": link,
                "content": content
            })
            time.sleep(1)

        return news_items

    except Exception as e:
        print("خطا در دریافت خبر:", e)
        return []

# تحلیل احساسات متن خبر
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "مثبت ✅"
    elif polarity < -0.1:
        return "منفی ❌"
    else:
        return "خنثی ⚪️"

# اجرای اصلی
def main():
    news = fetch_oilprice_news()
    if not news:
        send_telegram_message("⛔️ هیچ خبری برای تحلیل پیدا نشد.")
        return

    msg = f"📡 تحلیل {len(news)} خبر از OilPrice:\n"
    for item in news:
        sentiment = analyze_sentiment(item["content"])
        msg += f"\n📰 {item['title']}\n🔗 {item['link']}\n📊 احساس: {sentiment}\n"

    send_telegram_message(msg)

if __name__ == "__main__":
    main()
