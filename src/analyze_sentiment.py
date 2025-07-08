def simple_sentiment_analysis(headlines):
    positive_words = ["cut", "halt", "decline", "rise", "bullish", "demand"]
    negative_words = ["glut", "fall", "drop", "bearish", "oversupply"]

    sentiment_score = 0
    for title in headlines:
        for word in positive_words:
            if word in title.lower():
                sentiment_score += 1
        for word in negative_words:
            if word in title.lower():
                sentiment_score -= 1
    return sentiment_score
