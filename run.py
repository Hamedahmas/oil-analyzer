from src.fetch_news import get_all_headlines
from src.analyze_sentiment import simple_sentiment_analysis
from src.telegram_bot import send_telegram_message

headlines = get_all_headlines()
score = simple_sentiment_analysis(headlines)

summary = f"""🛢 تحلیل سریع بازار نفت

تعداد تیتر بررسی‌شده: {len(headlines)}
امتیاز سنتیمنت: {score}

📌 تیترهای اصلی:
- {chr(10).join(headlines)}

📡 سیستم تحلیل اتوماتیک | بروزرسانی هر 30 دقیقه
"""

send_telegram_message(summary)
