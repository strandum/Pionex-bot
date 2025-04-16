import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Coin config
ASSETS = {
    "solana": {
        "symbol": "SOL_USDT",
        "amount": 50,
        "last_buy": None,
    },
    "arbitrum": {
        "symbol": "ARB_USDT",
        "amount": 50,
        "last_buy": None,
    }
}

# Prisinnhenting via CoinGecko
def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        res = requests.get(url)
        return res.json()[coin_id]["usd"]
    except Exception as e:
        print(f"[{coin_id}] Feil ved prisinnhenting: {e}")
        return None

# Simulert ordre (bytt ut med ekte API-kall senere)
def place_order(symbol, side, amount):
    print(f"{side.upper()} {symbol} for {amount} USDT")

def main():
    print("Bot kjører – overvåker SOL og ARB...")
    price_history = {}

    while True:
        for coin in ASSETS:
            symbol = ASSETS[coin]["symbol"]
            amount = ASSETS[coin]["amount"]
            current_price = get_price(coin)

            if current_price is None:
                continue

            # Lagre pris-historikk for % beregning
            if coin not in price_history:
                price_history[coin] = [current_price]
            else:
                price_history[coin].append(current_price)
                if len(price_history[coin]) > 10:
                    price_history[coin].pop(0)

            if len(price_history[coin]) < 2:
    print(f"{coin.upper()} | Venter på mer historikk...")
    continue

avg_price = sum(price_history[coin][:-1]) / len(price_history[coin][:-1])
            print(f"{coin.upper()} | Nå: {current_price:.3f} | Endring: {change:.2f}%")

            last_buy = ASSETS[coin]["last_buy"]

            if change <= -2 and not last_buy:
                print(f"KJØPESIGNAL! {coin.upper()} falt {change:.2f}%, kjøper for {amount} USDT.")
                place_order(symbol, "buy", amount)
                ASSETS[coin]["last_buy"] = current_price

            elif last_buy:
                gain = (current_price - last_buy) / last_buy * 100
                if gain >= 5:
                    print(f"GEVINST! {coin.upper()} opp {gain:.2f}%, selger.")
                    place_order(symbol, "sell", amount)
                    ASSETS[coin]["last_buy"] = None
                elif gain <= -3:
                    print(f"STOP-LOSS! {coin.upper()} ned {gain:.2f}%, selger.")
                    place_order(symbol, "sell", amount)
                    ASSETS[coin]["last_buy"] = None

        time.sleep(60)

if __name__ == "__main__":
    main()