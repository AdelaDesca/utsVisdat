import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Dashboard Penjualan 2022", layout="wide")
st.title("Dashboard Penjualan 2022")

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "DataVisdat.csv"))

df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month_name()

page = st.sidebar.selectbox("Pilih Halaman", ["Campaign Trend 2022", "Mobile & Tablet Jazzwallet"])

if page == "Campaign Trend 2022":
    st.header("📈 Campaign Trend 2022")

    df_2022 = df[df['year'] == 2022]

    if df_2022.empty:
        st.warning("Tidak ada data untuk tahun 2022.")
    else:
        monthly_sales = df_2022.groupby('month')['after_discount'].sum().reset_index()

        order_bulan = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        monthly_sales['month'] = pd.Categorical(monthly_sales['month'], categories=order_bulan, ordered=True)
        monthly_sales = monthly_sales.sort_values('month')

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=monthly_sales, x='month', y='after_discount', marker='o', ax=ax)
        ax.set_title("Trend Penjualan per Bulan (2022)")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Total Penjualan (After Discount)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        total_sales = monthly_sales['after_discount'].sum()
        avg_sales = monthly_sales['after_discount'].mean()
        growth = ((monthly_sales['after_discount'].iloc[-1] - monthly_sales['after_discount'].iloc[0])
                  / monthly_sales['after_discount'].iloc[0]) * 100 if len(monthly_sales) > 1 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Penjualan 2022", f"{total_sales:,.0f}")
        c2.metric("Rata-rata Penjualan Bulanan", f"{avg_sales:,.0f}")
        c3.metric("Growth (%)", f"{growth:.2f}%")

        st.subheader("📌 Insight & Call to Action")
        if growth < 0:
            st.error("Terjadi penurunan penjualan — disarankan meningkatkan campaign digital atau promo di Q3.")
        else:
            st.success("Penjualan menunjukkan tren positif — pertahankan strategi dan perluas channel promosi.")

elif page == "Mobile & Tablet Jazzwallet":
    st.header("📱 Penjualan Mobile & Tablet (Jazzwallet)")

    df_2022 = df[df['year'] == 2022]
    df_mt = df_2022[
        (df_2022['payment_method'].str.lower() == 'jazzwallet') &
        (df_2022['category'].str.lower().isin(['mobile', 'tablet']))
    ]

    if df_mt.empty:
        st.warning("Tidak ada transaksi Mobile/Tablet dengan metode Jazzwallet pada 2022.")
    else:
        total_qty = df_mt['qty_ordered'].sum()
        total_customer = df_mt['customer_id'].nunique()

        c1, c2 = st.columns(2)
        c1.metric("Total Quantity", f"{total_qty}")
        c2.metric("Total Customer", f"{total_customer}")

        monthly_qty = df_mt.groupby(['month', 'category'])['qty_ordered'].sum().reset_index()
        monthly_qty['month'] = pd.Categorical(monthly_qty['month'], 
                                              categories=["January", "February", "March", "April", "May", "June",
                                                          "July", "August", "September", "October", "November", "December"],
                                              ordered=True)
        monthly_qty = monthly_qty.sort_values('month')

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=monthly_qty, x='month', y='qty_ordered', hue='category', ax=ax)
        ax.set_title("Jumlah Transaksi Mobile & Tablet (Jazzwallet) per Bulan")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        fig2, ax2 = plt.subplots()
        df_mt.groupby('category')['qty_ordered'].sum().plot.pie(autopct='%1.1f%%', ax=ax2, ylabel="")
        ax2.set_title("Proporsi Penjualan Mobile vs Tablet (Jazzwallet)")
        st.pyplot(fig2)

        st.subheader("📊 Insight & Rekomendasi")
        st.write("""
        - Mobile dan Tablet menunjukkan tren transaksi yang signifikan menggunakan Jazzwallet.  
        - Disarankan memperkuat promosi berbasis metode pembayaran digital seperti Jazzwallet,  
          terutama pada kategori dengan kontribusi tertinggi.  
        - Analisis lebih lanjut bisa difokuskan pada pola waktu transaksi untuk optimasi campaign musiman.

        """)
