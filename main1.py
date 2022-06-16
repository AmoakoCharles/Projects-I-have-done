import requests

from twilio.rest import Client

API_KAY = "a0ac057b964aec323230ae14e4e26dae"
account_sid = "ACe76d538593ad98d6470d001f3f10ad94"
auth_token = "ee8ba9d6caeac01a93e2794c29877a8d"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "a3e8324ffd2d46d0b0b76271dd0680a7"
STOCK_KEY = "2WJTLE6322A0L8M7"

parameters = {
    "q": COMPANY_NAME,
    "apikey": API_KEY

}

parameterse = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "60min",
    "apikey": STOCK_KEY
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
response = requests.get(url=STOCK_ENDPOINT, params=parameterse)
response.raise_for_status()
data = response.json()


new_dict = [value for (closer, value) in data["Time Series (Daily)"].items()]
yeste = float(new_dict[0]["4. close"])
before = float(new_dict[1]["4. close"])
diff = yeste - before


up_down = None
if diff > 0 or diff == 0:
    up_down = "🔺"
else:
    up_down = "🔻"
perc = round((diff / yeste) * 100)
description = []
headline = []
article = []


if abs(perc) >= 2:
    responses = requests.get(url=NEWS_ENDPOINT, params=parameters)
    responses.raise_for_status()
    datum = responses.json()
    news = [art for art in datum["articles"]]
    part = news[0:3]
    description = [des["description"] for des in part]
    headline = [head["title"] for head in part]
    for i in range(0, 3):
        article.append(f"{headline[i]}  {description[i]}")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"{STOCK_NAME}: {up_down} {perc}% \nHeadline: {headline[i]}\n"
                 f" Brief: {description[i]}",
            from_="+13305978901",
            to="+2330591552869"
        )
        print(message.status)


