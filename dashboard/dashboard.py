import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

day_df  = pd.read_csv("dashboard/day_df.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

hour_df  = pd.read_csv("dashboard/hour_df.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
st.sidebar.title("Bike Sharing Dataset Analysis")
st.sidebar.subheader("\n\n\n\n\n")
st.sidebar.write("Nama          : Humam Alwi Ahmad")
st.sidebar.write("Email         : humamalwi21@gmail.com")
st.sidebar.write("ID Dicoding   : humam_alwi_ahmad")





st.header("Bike Sharing Dataset Analysis :sparkles:")
st.subheader("\n\n")
#pertanyaan 1
st.subheader("Performa Jumlah Penyewaan Sepeda dan Pengguna Terdaftar")
tahun = st.selectbox("Tahun: ", ("2011", "2012"))

penyewaan_bulanan = day_df.resample(rule="ME", on="dteday").agg({
    "registered": "sum",
    "cnt": "sum"
})
penyewaan_bulanan['year'] = penyewaan_bulanan.index.year
penyewaan_bulanan.index = penyewaan_bulanan.index.strftime("%B")
penyewaan_bulanan = penyewaan_bulanan.reset_index()
penyewaan_bulanan.rename(columns={
    "dteday": "bulan",
    "registered": "penyewaan_terdaftar",
    "cnt": "penyewaan_total"
}, inplace=True)

penyewaan_tahun = penyewaan_bulanan[penyewaan_bulanan['year'] == int(tahun)]

plt.figure(figsize=(12, 7))
plt.plot(
    penyewaan_tahun["bulan"],
    penyewaan_tahun["penyewaan_total"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="Penyewaan Total"
)
plt.plot(
    penyewaan_tahun["bulan"],
    penyewaan_tahun["penyewaan_terdaftar"],
    marker='o',
    linewidth=2,
    color= "red",
    label="Penyewaan Terdaftar"
    
)
plt.title(f"Jumlah Penyewaan Bulanan pada Tahun {tahun}", loc="center", fontsize=20)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.legend(loc='upper right')
st.pyplot(plt)

st.subheader("\n\n\n")

#pertanyaan 2
st.subheader("Jumlah Penyewa Sepeda Terbanyak")

jam_penyewa_terbanyak = hour_df.groupby(["dteday", "hr"])["cnt"].sum().sort_values(ascending=False).reset_index()
jam_penyewa_terbanyak["datetime"] = pd.to_datetime(
    jam_penyewa_terbanyak["dteday"].dt.date.astype(str) + " " + jam_penyewa_terbanyak["hr"].astype(str) + ":00"
)
jam_penyewa_terbanyak["total penyewaan"] = jam_penyewa_terbanyak["cnt"]
jam_penyewa_terbanyak = jam_penyewa_terbanyak.drop(columns=["dteday", "hr", "cnt"])
jam_penyewa_terbanyak.head()

penyewa_terbanyak = jam_penyewa_terbanyak.sort_values(by="total penyewaan", ascending=False).head(5)


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="total penyewaan", y="datetime", data=penyewa_terbanyak, palette=colors)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title(" ", loc="center", fontsize=18)
ax.tick_params(axis='y', labelsize=15)

plt.suptitle("Performa Penyewaan Sepeda per Jam", fontsize=20)
st.pyplot(plt)


st.subheader("\n\n\n")
#pertanyaan 3
st.subheader("Pengaruh Suhu yang Dirasa Terhadap Jumlah Penyewaan Sepeda")

suhu_utk_penyewaan = day_df.groupby(by="atemp_group").agg({
    "registered": "sum",
    "casual": "sum",
    "cnt": "sum"
}).reset_index()

suhu_utk_penyewaan.rename(columns={
    "registered": "penyewaan_terdaftar",
    "casual": "penyewaan_kasual",
    "cnt": "total_penyewaan"
}, inplace=True)

average_penyewaan = suhu_utk_penyewaan.groupby("atemp_group")["total_penyewaan"].mean().reset_index()

plt.figure(figsize=(10, 5))

sns.barplot(
    y="total_penyewaan", 
    x="atemp_group",
    data=average_penyewaan,
    color="#72BCD4"
)
plt.title("Rerata Total Penyewaan Berdasarkan Suhu yang Dirasa (atemp)", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
st.pyplot(plt)


st.subheader("\n\n\n")
st.caption("Copyright © Humam Alwi Ahmad 2024")
