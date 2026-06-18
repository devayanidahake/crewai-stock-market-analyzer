import requests
import os

API_KEY = os.getenv("NEWS_API_KEY")
# "8159430db19c4a019f3560baec7043d6"


def get_market_news():

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=(nifty OR sensex OR stock market OR RBI OR Fed OR inflation OR earnings)"
        f"&language=en"
        f"&sortBy=publishedAt"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    headlines = []

    for article in data.get("articles", [])[:10]:
        headlines.append(
            {
                "title": article["title"],
                "source": article["source"]["name"],
                "published": article["publishedAt"],
            }
        )

    return headlines
