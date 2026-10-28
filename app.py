import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Perodua Sarinani Motors - Quotation",
    page_icon="🚗",
    layout="centered",
)

# Guna nama fail logo sebenar yang ada dalam GitHub anda
if os.path.exists("sarinani_motors_logo.png"):
  st.image("sarinani_motors_logo.png", use_container_width=True)
elif os.path.exists("Perodua-Logo.png"):
  st.image("Perodua-Logo.png", use_container_width=True)

st.title("🚗 Sistem Pilihan Servis Kenderaan (Perodua Sarinani Motors)")
st.write(
    "Sila pilih model kenderaan dan komponen servis pilihan anda di bawah:"
)

nama_fail_excel = "BASIC SERVICE NIZAR.xlsx"

if os.path.exists(nama_fail_excel):
  df = pd.read_excel(nama_fail_excel, sheet_name=0)

  model_list = [
      col
      for col in df.columns
      if col
      not in [
          "MODEL",
          "ADDITIONAL SERVICE",
          "PRICE",
          "Unnamed: 1",
          "Unnamed: 2",
      ]
  ]

  model_pilihan = st.selectbox("Pilih Model Kenderaan Anda:", model_list)
  total_harga = 0.0

  st.subheader(f"📋 Senarai Servis Asas untuk: {model_pilihan}")

  for index, row in df.iterrows():
    item_servis = row["MODEL"]

    if (
        pd.isna(item_servis)
        or str(item_servis).strip() == ""
        or "ADDITIONAL" in str(item_servis).upper()
    ):
      break

    harga = row[model_pilihan]
    nama_bersih = str(item_servis).replace("*", "").strip()

    if nama_bersih.upper() != "SUBTOTAL":
      if pd.notna(harga):
        try:
          harga_float = float(harga)
          total_harga += harga_float

          col1, col2 = st.columns([3, 1])
          with col1:
            st.write(f"• **{nama_bersih}**")
          with col2:
            st.write(f"**RM {harga_float:.2f}**")

          if "JAS WSSF" in nama_bersih.upper():
            with st.expander(f"ℹ️ Ketik untuk lihat penerangan: {nama_bersih}"):
              st.write(
                  "• **JAS**: Pelaksanaan Caj Pelupusan Sisa Berjadual"
                  " (Environment Waste Fee) minimum sebanyak RM5.00.\n•"
                  " **WSSF**: Pelaksanaan Caj Bahan Consumable dan Sanitasi"
                  " Bengkel."
              )

        except ValueError:
          pass

  st.subheader("🛠️ Servis Tambahan Pilihan (Optional)")

  is_addon_section = False
  for index, row in df.iterrows():
    item_servis = str(row["MODEL"]).strip()

    if "ADDITIONAL" in item_servis.upper():
      is_addon_section = True
      continue

    if is_addon_section and pd.notna(row["MODEL"]) and row["MODEL"] != "":
      nama_addon = str(row["MODEL"]).replace("*", "").strip()
      harga_addon = row[df.columns[1]]

      if pd.notna(harga_addon) and str(harga_addon).strip() != "":
        try:
          harga_addon_float = float(harga_addon)

          pilih = st.checkbox(
              f"Tambah **{nama_addon}** (+RM {harga_addon_float:.2f})",
              key=f"addon_row_{index}",
          )
          if pilih:
            total_harga += harga_addon_float

          if "OZONE" in nama_addon.upper():
            with st.expander(f"ℹ️ Ketik untuk lihat penerangan: {nama_addon}"):
              st.write(
                  "Rawatan ozon untuk membunuh bakteria, kulat, dan menyahbau"
                  " kurang menyenangkan di dalam kabin kereta."
              )

        except ValueError:
          pass

  st.markdown("---")
  st.subheader("💰 Anggaran Jumlah Keseluruhan (Grand Total)")
  st.success(f"**RM {total_harga:.2f}**")

  if st.button("Cetak / Sahkan Sebut Harga"):
    st.balloons()
    st.info(
        "Sebut harga berjaya direkodkan! Sila tunjukkan skrin ini kepada"
        " Service Advisor."
    )

else:
  st.error(f"Fail '{nama_fail_excel}' tidak dijumpai di dalam folder!")
