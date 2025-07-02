import requests
import pandas as pd
from datetime import datetime
import os

CSV_FILE = "crypto_data.csv"

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }

    scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("❌ Failed to fetch data")
        return

    data = response.json()
    all_rows = []

    for coin in data:
        current_price = coin.get('current_price', 0.0)
        price_change = coin.get('price_change_24h') or 0.0
        open_est = current_price - price_change

        row = [
            coin.get('name'),
            coin.get('symbol'),
            current_price,
            coin.get('high_24h'),
            coin.get('low_24h'),
            open_est,
            coin.get('total_volume'),
            scrape_time
        ]
        all_rows.append(row)

    df = pd.DataFrame(all_rows, columns=[
        "Name", "Symbol", "Current Price", "High 24h", "Low 24h",
        "Open (estimated)", "Volume", "Scraped At"
    ])

    file_exists = os.path.isfile(CSV_FILE)
    df.to_csv(CSV_FILE, mode='a', index=False, header=not file_exists)
    print(f"[{scrape_time}] ✅ Saved {len(all_rows)} rows")

# Run once when script starts
fetch_crypto_data()
