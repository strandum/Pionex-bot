import os
import time

# Dummy bot logic – just logs price every X seconds
def run_bot():
    print("Starting Pionex bot...")
    api_key = os.getenv("PIONEX_API_KEY")
    secret_key = os.getenv("PIONEX_SECRET_KEY")

    if not api_key or not secret_key:
        print("API keys missing! Add them as environment variables.")
        return

    while True:
        print("Monitoring market... (pretend I'm doing smart trades)")
        # Her kan vi hente prisdata eller sende ordre senere
        time.sleep(30)

if __name__ == "__main__":
    run_bot()
