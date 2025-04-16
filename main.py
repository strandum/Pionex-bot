import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

ASSETS = {
    "solana": {
        "symbol": "SOL_USDT",
        "amount": 50,
        "last_buy": None
    },
    "arbitrum": {
        "symbol": "ARB_USDT",
        "amount": 50,
        "last_buy": None
    }
}

price_history = {}

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        res = requests.get(url)
        return res.json()[coin_id]["usd"]
    except Exception as e:
        print(f"[{coin_id.upper()}] Feil ved prisinnhenting: {e}")
        return None

def place_order(symbol, side, amount):
    print(f"{side.upper()} {symbol} for {amount} USDT")

def main():
    print("Bot kjører... overvåker SOL og ARB")
    while True:
        for coin in ASSETS:
            symbol = ASSETS[coin]["symbol"]
            amount = ASSETS[coin]["amount"]
            current_price = get_price(coin)

            if current_price is None:
                continue

            # Prislogg for % beregning
            if coin not in price_history:
                price_history[coin] = [current_price]
                print(f"{coin.upper()} | Venter på mer historikk...")
                continue
            else:
                price_history[coin].append(current_price)
                if len(price_history[coin]) > 10:
                    price_history[coin].pop(0)

            avg_price = sum(price_history[coin][:-1]) / len(price_history[coin][:-1])
            change = (current_price - avg_price) / avg_price * 100
            print(f"{coin.upper()} | Nå: {current_price:.3f} | Endring: {change:.2f}%")

            last_buy = ASSETS[coin]["last_buy"]

            if change <= -2 and not last_buy:
                print(f"KJØPESIGNAL for {coin.upper()}! Pris falt {change:.2f}% – kjøper for {amount} USDT.")
                place_order(symbol, "buy", amount)
                ASSETS[coin]["last_buy"] = current_price

            elif last_buy:
                gain = (current_price - last_buy) / last_buy * 100
                if gain >= 5:
                    print(f"GEVINST! {coin.upper()} opp {gain:.2f}% – selger.")
                    place_order(symbol, "sell", amount)
                    ASSETS[coin]["last_buy"] = None
                elif gain <= -3:
                    print(f"STOP-LOSS! {coin.upper()} ned {gain:.2f}% – selger.")
                    place_order(symbol, "sell", amount)
                    ASSETS[coin]["last_buy"] = None

        time.sleep(60)

if __name__ == "__main__":
    main()