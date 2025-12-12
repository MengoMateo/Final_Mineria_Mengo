import streamlit as st
import plotly.express as px
import pandas as pd
from preprocess import preprocess_data

# ----------------------------
#   TÍTULO DEL DASHBOARD
# ----------------------------
st.title("📊 Dashboard de Bitcoin y Ethereum")

# ----------------------------
#   CARGAR Y PROCESAR DATOS
# ----------------------------
df = preprocess_data()

# Asegurar datetime
df["date"] = pd.to_datetime(df["date"])

st.subheader("📌 Vista previa de datos")
st.write(df.head())

# ----------------------------
#   GRÁFICO BTC
# ----------------------------
st.subheader("📈 Bitcoin – Precio y Medias Móviles")
fig_btc = px.line(
    df,
    x="date",
    y=["price_btc", "ma7_btc", "ma30_btc"],
    labels={"date": "Fecha", "value": "Precio USD"},
    title="Bitcoin (BTC): Precio y Medias Móviles"
)
st.plotly_chart(fig_btc)

# ----------------------------
#   GRÁFICO ETH
# ----------------------------
st.subheader("📉 Ethereum – Precio y Medias Móviles")
fig_eth = px.line(
    df,
    x="date",
    y=["price_eth", "ma7_eth", "ma30_eth"],
    labels={"date": "Fecha", "value": "Precio USD"},
    title="Ethereum (ETH): Precio y Medias Móviles"
)
st.plotly_chart(fig_eth)

# ----------------------------
#   SELECTOR DE FECHA
# ----------------------------
st.subheader("🔍 Consultar precio por fecha")

selected_date = st.date_input(
    "Selecciona una fecha:",
    min_value=df["date"].min().date(),
    max_value=df["date"].max().date(),
    value=df["date"].max().date()
)

# Fila exacta
row = df[df["date"].dt.date == selected_date]

# Mostrar resultados
if not row.empty:
    st.success(f"📅 Datos del {selected_date}:")
    st.write(f"🟦 **Bitcoin (BTC):** ${row.iloc[0]['price_btc']:.2f}")
    st.write(f"🟪 **Ethereum (ETH):** ${row.iloc[0]['price_eth']:.2f}")
else:
    st.warning("⚠ No hay datos exactos para esa fecha (puede ser que el API no devolvió ese día exacto).")
