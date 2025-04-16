import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

headers = {
    "PIONEX-KEY": API_KEY,
    "PIONEX-SECRET": API_SECRET
}

BASE_URL = "https://api.pionex.com"
price_history = {}
ASSETS = {
    "SOL": {"last_buy": False},
    "ARB": {"last_buy": False}
}

def get_price(symbol):
    url = f"https://api.pionex.com/api/v1/market/ticker?symbol={symbol}"
    try:
        res = requests.get(url)
        data = res.json()
        print(f"API response for {symbol}:", data)

        if "price" in data:
            return float(data["price"])
        else:
            raise ValueError(f"Mangler 'price' i responsen for {symbol}: {data}")
    except Exception as e:
        print(f"Feil ved henting av pris for {symbol}: {e}")
        raise e
def main():
    coins = ["SOL", "ARB"]
    while True:
        for coin in coins:
            symbol = f"{coin.lower()}_usdt"
            current_price = get_price(symbol))
            print(f"Sjekker {coin.upper()}...")

            # Pris-historikk lagring
            if coin not in price_history:
                price_history[coin] = [current_price]
            else:
                price_history[coin].append(current_price)
                if len(price_history[coin]) > 5:
                    price_history[coin].pop(0)

            # Vent hvis for lite historikk
            if len(price_history[coin]) < 2:
                print(f"{coin.upper()} | Venter på mer historikk...")
                continue

            avg_price = sum(price_history[coin][:-1]) / (len(price_history[coin]) - 1)
            change = (current_price - avg_price) / avg_price * 100

            print(f"{coin.upper()} | Nå: {current_price:.3f} | Endring: {change:.2f}%")

            last_buy = ASSETS[coin]["last_buy"]

            if change <= -2 and not last_buy:
                print(f"KJØPESIGNAL! {coin.upper()} ({current_price:.3f})")
                ASSETS[coin]["last_buy"] = True

            if change >= 2 and last_buy:
                print(f"SELGSIGNAL! {coin.upper()} ({current_price:.3f})")
                ASSETS[coin]["last_buy"] = False

        time.sleep(30)

if __name__ == "__main__":
    print("Bot kjører – overvåker SOL og ARB...")
    main()