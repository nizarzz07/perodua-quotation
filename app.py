import os
import pandas as pd
import streamlit as st

st.title("🚗 Sistem Pilihan Servis Kenderaan (Perodua Sarinani Motors Bukit Mertajam)")
st.write(
    "Sila pilih model kenderaan dan komponen servis pilihan anda di bawah:"
)

nama_fail_excel = "BASIC SERVICE NIZAR.xlsx"

if os.path.exists(nama_fail_excel):
  # Baca fail Excel dari Sheet pertama
  df = pd.read_excel(nama_fail_excel, sheet_name=0)

  # Cari senarai model kenderaan
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

  # 1. Pelanggan pilih model kereta
  model_pilihan = st.selectbox("Pilih Model Kenderaan Anda:", model_list)

  total_harga = 0.0

  # Fungsi kecil untuk beri penerangan ringkas bagi setiap servis
  def dapatkan_penerangan(nama_item):
    nama = nama_item.upper()
    if "MINYAK ENGINE" in nama:
      return (
          "Minyak enjin berkualiti tinggi untuk melindungi enjin, melancarkan"
          " pergerakan komponen, dan menjaga prestasi pemanduan."
      )
    elif "OIL FILTER" in nama:
      return (
          "Menapis kotoran dan serpihan halus daripada minyak enjin supaya"
          " enjin sentiasa bersih dan tahan lama."
      )
    elif "GASKET" in nama:
      return (
          "Getah penutup skru minyak hitam untuk mengelakkan berlakunya"
          " sebarang kebocoran minyak."
      )
    elif "INJECTOR CLEANER" in nama:
      return (
          "Cecair pencuci khas untuk membersihkan sistem injektor bahan api,"
          " menjimatkan minyak,mencuci carbon deposit dalam enjin dan melancarkan pecutan."
      )
    elif "WINDSHIELD WASHER" in nama:
      return (
          "Cecair pencuci cermin kereta untuk memastikan pandangan lebih jelas"
          " dan membuang kesan degil pada cermin."
      )
    elif "JAS WSSF" in nama:
      return "JAS-Pelaksanaan Caj Pelupusan Sisa Berjadual (Environment Waste Fee) Minimum sebanyak RM5.00/WSSF-Pelaksanaan Caj Bahan Consumable Dan Sanitasi Bengkel"
    elif "LABOUR SERVICE" in nama:
      return "Upah kerja pemasangan dan pemeriksaan oleh MECHANIC BERTAULIAH."
    elif "ALIGNMENT" in nama:
      return (
          "(alignment & balancing) untuk memastikan steering"
          " stabil dan tayar tidak haus sebelah."
      )
    elif "OZONE" in nama:
      return (
          "Rawatan ozon untuk membunuh bakteria, kulat, dan menyahbau kurang"
          " menyenangkan di dalam kabin kereta."
      )
    elif "CAR WASH" in nama:
      return "Servis membasuh luar dan dalam kereta supaya bersih berkilat."
    elif "THROTTLE BODY" in nama:
      return (
          "Servis cuci komponen Throttle Body untuk melancarkan semula"
          " kemasukan angin ke enjin dan mengelakkan enjin 'regat'."
      )
    else:
      return "Komponen atau servis rasmi untuk penjagaan kenderaan Perodua anda."

  # --- BAHAGIAN 1: SERVIS ASAS ---
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

          # Paparkan nama item & harga, disertakan butang expander untuk nota/penerangan
          col1, col2 = st.columns([3, 1])
          with col1:
            st.write(f"• **{nama_bersih}**")
          with col2:
            st.write(f"**RM {harga_float:.2f}**")

          # Butang tekan untuk lihat penerangan
          with st.expander(f"ℹ️ Ketik untuk lihat penerangan: {nama_bersih}"):
            st.write(dapatkan_penerangan(nama_bersih))

        except ValueError:
          pass

  # --- BAHAGIAN 2: ADDITIONAL SERVICE (TAMBAHAN) ---
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

          # Kotak pilihan untuk servis tambahan
          pilih = st.checkbox(
              f"Tambah **{nama_addon}** (+RM {harga_addon_float:.2f})",
              key=f"addon_row_{index}",
          )
          if pilih:
            total_harga += harga_addon_float

          # Butang tekan untuk lihat penerangan servis tambahan
          with st.expander(f"ℹ️ Ketik untuk lihat penerangan: {nama_addon}"):
            st.write(dapatkan_penerangan(nama_addon))

        except ValueError:
          pass

  # 3. Paparan Jumlah Keseluruhan
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
  st.error(f"⚠️ Fail '{nama_fail_excel}' tidak dijumpai di dalam folder!")
