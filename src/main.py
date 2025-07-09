import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

TELEGRAM_TOKEN = "7754260268:AAE2JjAal8Di-qOTOUf0lBRN4FNNl3VrUo4"
TELEGRAM_CHAT_ID = "-1002233437580"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    print("ارسال شد:", response.status_code)

def fetch_oilprice_news():
    url = "https://oilprice.com/latest-energy-news/world-news/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.select("div.categoryArticle")
    news_items = []

    for article in articles[:5]:  # حداکثر 5 خبر اول
        title_tag = article.select_one("h2.categoryArticle__title")
        link_tag = article.select_one("a[href]")
        excerpt_tag = article.select_one("p.categoryArticle__excerpt")

        if title_tag and link_tag:
            title = title_tag.text.strip()
            link = link_tag['href']
            excerpt = excerpt_tag.text.strip() if excerpt_tag else ""

            news_items.append({
                "title": title,
                "link": link,
                "content": excerpt
            })

    return news_items

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return polarity

def main():
    news = fetch_oilprice_news()
    if not news:
        send_telegram_message("🛢 تحلیل سریع بازار نفت\nتعداد تیتر بررسی‌شده: 0\nامتیاز سنتیمنت: 0\n\n📌 تیترهای اصلی:\n- \n\n📡 سیستم تحلیل اتوماتیک | بروزرسانی هر 30 دقیقه")
        return

    msg = f"🛢 تحلیل سریع بازار نفت\nتعداد تیتر بررسی‌شده: {len(news)}\n\n"
    total_polarity = 0

    for item in news:
        polarity = analyze_sentiment(item['content'])
        total_polarity += polarity
        sentiment_label = "مثبت ✅" if polarity > 0.1 else ("منفی ❌" if polarity < -0.1 else "خنثی ⚪️")
        msg += f"📰 {item['title']}\n📊 احساس: {sentiment_label}\n🔗 {item['link']}\n\n"

    avg_sentiment = round(total_polarity / len(news), 2)
    msg += f"امتیاز سنتیمنت میانگین: {avg_sentiment}\n\n📡 سیستم تحلیل اتوماتیک | بروزرسانی هر 30 دقیقه"

    send_telegram_message(msg)

if __name__ == "__main__":
    main()
