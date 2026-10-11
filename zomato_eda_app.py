import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Zomato Bangalore Restaurants EDA", page_icon="🍽️", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("zomato_cleaned.csv")
    return df

df = load_data()

st.title("🍽️ Zomato Bangalore Restaurants - Keşifçi Veri Analizi")
st.write("Bu uygulama, Bangalore'daki restoranların maliyet, puan, konum ve hizmet türlerine göre analizini sunar.")

# Sidebar Filtreleri
st.sidebar.header("Filtreleme Paneli")
locations = ["Tümü"] + sorted(df['location'].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("Bölge (Location) Seçin", locations)

online_order_filter = st.sidebar.selectbox("Online Sipariş", ["Tümü", "Yes", "No"])
book_table_filter = st.sidebar.selectbox("Masa Rezervasyonu", ["Tümü", "Yes", "No"])

# Veriyi filtreleme
filtered_df = df.copy()
if selected_location != "Tümü":
    filtered_df = filtered_df[filtered_df['location'] == selected_location]
if online_order_filter != "Tümü":
    filtered_df = filtered_df[filtered_df['online_order'] == online_order_filter]
if book_table_filter != "Tümü":
    filtered_df = filtered_df[filtered_df['book_table'] == book_table_filter]

st.subheader(f"Filtrelenen Restoran Sayısı: {len(filtered_df):,}")

# 1. Puan Dağılımı
st.markdown("### ⭐ Restoran Puanları (Ratings) Dağılımı")
valid_ratings = filtered_df[filtered_df['ratings'] > 0]
if not valid_ratings.empty:
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(valid_ratings['ratings'], bins=20, kde=True, color='crimson', ax=ax)
    ax.set_xlabel("Puan")
    ax.set_ylabel("Restoran Sayısı")
    st.pyplot(fig)
else:
    st.warning("Bu filtreye uygun puan verisi bulunamadı.")

# 2. Maliyet Dağılımı ve En Popüler Restoran Türleri
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💰 İki Kişilik Ortalama Maliyet Dağılımı")
    valid_cost = filtered_df[(filtered_df['cost_for_two'] > 0) & (filtered_df['cost_for_two'] < 4000)]
    if not valid_cost.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(valid_cost['cost_for_two'], bins=30, color='darkred', ax=ax)
        ax.set_xlabel("Maliyet (2 Kişilik)")
        ax.set_ylabel("Frekans")
        st.pyplot(fig)

with col2:
    st.markdown("### 🏆 En Yaygın İlk 10 Restoran Türü")
    top_types = filtered_df['rest_type'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=top_types.values, y=top_types.index, palette='rocket', ax=ax)
    ax.set_xlabel("Restoran Sayısı")
    ax.set_ylabel("Tür")
    st.pyplot(fig)