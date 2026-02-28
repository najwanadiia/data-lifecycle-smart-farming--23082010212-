import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Kelembaban", layout="wide")
st.title("🌾 Dashboard Smart Farming (Dataset 2)")
st.write("Monitoring Sensor Kelembaban Tanah - Tugas 2")

try:
    df = pd.read_csv("outputs/cleaned_data.csv")
except:
    st.error("Waduh datanya ga kebaca. Udah ditaruh di folder outputs/cleaned_data.csv belum?")
    st.stop()

kelembaban_sekarang = df['moisture0'].iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚨 Alert System")
    batas_aman = 40.0
    
    if kelembaban_sekarang < batas_aman:
        st.error(f"WASPADA: Level kelembaban cuma {kelembaban_sekarang}. Tanah kering, waktunya nyalain pompa air!")
    else:
        st.success(f"AMAN: Level kelembaban oke di angka {kelembaban_sekarang}.")
        
with col2:
    st.markdown("### 💧 Gauge Kelembaban (Sensor 0)")
    fig1 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = kelembaban_sekarang,
        title = {'text': "Moisture 0"},
        gauge = {
            'axis': {'range': [0, 100]}, # asumsikan max 100
            'bar': {'color': "dodgerblue"},
            'steps': [
                {'range': [0, 40], 'color': "tomato"},
                {'range': [40, 70], 'color': "gold"},
                {'range': [70, 100], 'color': "limegreen"}
            ]
        }
    ))
    st.plotly_chart(fig1, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.markdown("### 📈 Tren Sensor Kelembaban")
    data_tren = df[['moisture0', 'moisture1']].tail(100).reset_index(drop=True)
    st.line_chart(data_tren)

with col4:
    st.markdown("### 🔥 Heatmap Korelasi")
    fig2, ax = plt.subplots(figsize=(8,6))
  
    kolom_angka = df.select_dtypes(include=['number'])
    sns.heatmap(kolom_angka.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig2)
