import requests
from bs4 import BeautifulSoup

def get_oilprice_headlines():
    url = "https://oilprice.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = [a.text.strip() for a in soup.select('div.categoryArticle__content a')][:5]
    return headlines

def get_reuters_headlines():
    url = "https://www.reuters.com/markets/commodities/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = [a.text.strip() for a in soup.select('a[data-testid="Heading"]')][:5]
    return headlines

def get_all_headlines():
    return get_oilprice_headlines() + get_reuters_headlines()
