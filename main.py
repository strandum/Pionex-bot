import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COINCAP_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

price_history = {}
ASSETS = {
    "solana": {"last_buy": False, "name": "SOL"},
    "arbitrum": {"last_buy": False, "name": "ARB"}
}

def get_price(coin_id):
    url = f"https://api.coincap.io/v2/assets/{coin_id}"
    try:
        res = requests.get(url, headers=headers)
        data = res.json()
        print(f"API response for {coin_id}:", data)

        if "data" in data and "priceUsd" in data["data"]:
            return float(data["data"]["priceUsd"])
        else:
            raise ValueError(f"Mangler pris i responsen for {coin_id}: {data}")
    except Exception as e:
        print(f"Feil ved henting av pris for {coin_id}: {e}")
        raise e

def main():
    print("Bot kjører – overvåker SOL og ARB...")
    while True:
        for coin_id, coin_info in ASSETS.items():
            current_price = get_price(coin_id)
            name = coin_info["name"]
            print(f"Sjekker {name}...")

            # Pris-historikk lagring
            if coin_id not in price_history:
                price_history[coin_id] = [current_price]
            else:
                price_history[coin_id].append(current_price)
                if len(price_history[coin_id]) > 5:
                    price_history[coin_id].pop(0)

            # Vent hvis for lite historikk
            if len(price_history[coin_id]) < 2:
                print(f"{name} | Venter på mer historikk...")
                continue

            avg_price = sum(price_history[coin_id][:-1]) / (len(price_history[coin_id]) - 1)
            change = (current_price - avg_price) / avg_price * 100

            print(f"{name} | Nå: {current_price:.3f} | Endring: {change:.2f}%")

            last_buy = ASSETS[coin_id]["last_buy"]

            if change <= -2 and not last_buy:
                print(f"KJØPESIGNAL! {name} ({current_price:.3f})")
                ASSETS[coin_id]["last_buy"] = True

            if change >= 2 and last_buy:
                print(f"SELGSIGNAL! {name} ({current_price:.3f})")
                ASSETS[coin_id]["last_buy"] = False

        time.sleep(30)

if __name__ == "__main__":
    main()
