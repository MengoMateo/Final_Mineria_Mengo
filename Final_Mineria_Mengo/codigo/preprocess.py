import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, "datos", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "datos", "processed")

def preprocess_data():

    path_btc = os.path.join(DATA_RAW, "bitcoin.json")
    path_eth = os.path.join(DATA_RAW, "ethereum.json")

    # Carga de datos
    btc = pd.read_json(path_btc)
    eth = pd.read_json(path_eth)

    # Renombrar
    btc = btc.rename(columns={"price": "price_btc"})
    eth = eth.rename(columns={"price": "price_eth"})

    # Medias móviles BTC
    btc["ma7_btc"] = btc["price_btc"].rolling(7).mean()
    btc["ma30_btc"] = btc["price_btc"].rolling(30).mean()

    # Medias móviles ETH
    eth["ma7_eth"] = eth["price_eth"].rolling(7).mean()
    eth["ma30_eth"] = eth["price_eth"].rolling(30).mean()

    # Merge por fecha
    df = pd.merge(btc, eth, on="date", how="inner")

    # Ordenar y limpiar
    df = df.sort_values("date").dropna()

    # Guardar CSV
    os.makedirs(DATA_PROCESSED, exist_ok=True)
    output_path = os.path.join(DATA_PROCESSED, "crypto_prices.csv")
    df.to_csv(output_path, index=False)

    print(f"Archivo procesado guardado en: {output_path}")
    return df


if __name__ == "__main__":
    preprocess_data()
