import requests
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, "datos", "raw")

def fetch_price_history(coin_id, filename):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    
    params = {
        "vs_currency": "usd",
        "days": "365"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Error al obtener datos de {coin_id}: {response.text}")

    data = response.json()
    prices = data["prices"]  # formato: [timestamp, price]

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["date", "price"]]

    output_path = os.path.join(DATA_RAW, filename)
    df.to_json(output_path, orient="records")
    print(f"Archivo guardado: {output_path}")


if __name__ == "__main__":
    os.makedirs(DATA_RAW, exist_ok=True)
    fetch_price_history("bitcoin", "bitcoin.json")
    fetch_price_history("ethereum", "ethereum.json")
    print("Descarga completa ✔")
