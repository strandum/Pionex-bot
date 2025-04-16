import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# API-nøkler
API_KEY = os.getenv("PIONEX_API_KEY")
API_SECRET = os.getenv("PIONEX_API_SECRET")

# Konfigurasjon
ASSETS = {
    "solana": {
        "symbol": "SOL_USDT",
        "amount": 60,
        "last_buy": None,
    },
    "arbitrum": {
        "symbol": "ARB_USDT",
        "amount": 40,
        "last_buy": None,
    }
}

HEADERS = {
    "PIONEX-KEY": API_KEY,
    "PIONEX-SECRET": API_SECRET
}

# CoinGecko API
def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        res = requests.get(url).json()
        return res[coin_id]["usd"]
    except Exception as e:
        print("Feil ved prisinnhenting:", e)
        return None

# Simulert kjøp (du kan koble til Pionex senere)
def place_order(symbol, side, amount):
    print(f"{side.upper()} {symbol} for {amount} USDT")

# Hovedloop
def main():
    print("Bot kjører...")
    history = {}

    while True:
        for coin in ASSETS:
            symbol = ASSETS[coin]["symbol"]
            amount = ASSETS[coin]["amount"]
            price = get_price(coin)

            if price is None:
                continue

            # Lagre første pris
            if coin not in history:
                history[coin] = [price]
            else:
                history[coin].append(price)
                if len(history[coin]) > 10:
                    history[coin].pop(0)

            avg_old = sum(history[coin][:-1]) / len(history[coin][:-1]) if len(history[coin]) > 1 else price
            change = (price - avg_old) / avg_old * 100

            print(f"{coin.upper()}: Nå: {price:.2f}, Endring: {change:.2f}%")

            last_buy = ASSETS[coin]["last_buy"]

            if change <= -2 and not last_buy:
                print(f"Kjøper {coin.upper()}!")
                place_order(symbol, "buy", amount)
                ASSETS[coin]["last_buy"] = price

            elif last_buy:
                gain = (price - last_buy) / last_buy * 100
                if gain >= 5:
                    print(f"Selger {coin.upper()} med gevinst på {gain:.2f}%")
                    place_order(symbol, "sell", amount)
                    ASSETS[coin]["last_buy"] = None
                elif gain <= -3:
                    print(f"Selger {coin.upper()} med tap på {gain:.2f}% (stop loss)")
                    place_order(symbol, "sell", amount)
                    ASSETS[coin]["last_buy"] = None

        time.sleep(60)

if __name__ == "__main__":
    main()
