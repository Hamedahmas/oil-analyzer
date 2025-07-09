import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import time

# ✅ تنظیمات تلگرام
TELEGRAM_TOKEN = "7754260268:AAE2JjAal8Di-qOTOUf0lBRN4FNNl3VrUo4"
TELEGRAM_CHAT_ID = "-1002233437580"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    print("ارسال به تلگرام:", response.status_code)

def fetch_oilprice_news():
    news_url = "https://oilprice.com/latest-energy-news/world-news/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(news_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # گرفتن همه <a> هایی که داخلشون <h2 class="categoryArticle__title"> هست
        articles = soup.select("a:has(h2.categoryArticle__title)")

        news_items = []

        for article in articles[:5]:
            title_tag = article.select_one("h2.categoryArticle__title")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            link = article['href']

            # دریافت متن کامل خبر
            article_res = requests.get(link, headers=headers, timeout=10)
            article_soup = BeautifulSoup(article_res.text, "html.parser")
            paragraphs = article_soup.select(".article-content p")
            content = " ".join(p.text for p in paragraphs)

            news_items.append({
                "title": title,
                "link": link,
                "content": content
            })

            time.sleep(1)  # جلوگیری از بلاک شدن

        return news_items

    except Exception as e:
        print("خطا در دریافت خبر:", e)
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
    news = fetch_oilprice_news()
    if not news:
        send_telegram_message("🛢 تحلیل سریع بازار نفت\nتعداد تیتر بررسی‌شده: 0\nامتیاز سنتیمنت: 0\n\n📡 سیستم تحلیل اتوماتیک | بروزرسانی هر 30 دقیقه")
        return

    msg = f"🛢 تحلیل سریع بازار نفت\nتعداد تیتر بررسی‌شده: {len(news)}\n"
    sentiment_total = 0

    for item in news:
        sentiment = analyze_sentiment(item['content'])
        msg += f"\n📰 {item['title']}\n📊 احساس: {sentiment}\n🔗 {item['link']}\n"
        blob = TextBlob(item['content'])
        sentiment_total += blob.sentiment.polarity

    avg_sentiment = round(sentiment_total / len(news), 2)
    msg += f"\nامتیاز سنتیمنت میانگین: {avg_sentiment}"
    msg += "\n\n📡 سیستم تحلیل اتوماتیک | بروزرسانی هر 30 دقیقه"

    send_telegram_message(msg)

if __name__ == "__main__":
    main()
