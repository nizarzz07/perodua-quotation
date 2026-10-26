import os
import pandas as pd
import streamlit as st

st.title("🚗 Sistem Pilihan Servis Kenderaan (Perodua Sarinani Motors)")
st.write("Sila pilih model kenderaan dan komponen servis pilihan anda di bawah:")

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

  # --- BAHAGIAN 1: SERVIS ASAS & PILIHAN ---
  st.subheader(f"📋 Senarai Servis untuk: {model_pilihan}")

  # Senarai item optional (lalai = False / tidak dipilih, boleh tolak atau terima)
  optional_items = ["INJECTOR CLEANER", "WINDSHIELD WASHER FLUID", "JAS WSSF"]

  for index, row in df.iterrows():
    item_servis = row["MODEL"]

    # Hentikan gelung jika berjumpa baris kosong atau bahagian 'ADDITIONAL SERVICE'
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

          # Jika item optional, jadikan checkbox dengan nilai lalai False (tidak dipilih / boleh tolak)
          if any(opt in nama_bersih.upper() for opt in optional_items):
            pilih_item = st.checkbox(
                f"{nama_bersih} (+RM {harga_float:.2f})",
                value=False,
                key=f"opt_item_{index}",
            )
            if pilih_item:
              total_harga += harga_float
          else:
            # Servis wajib kekal dimasukkan terus
            st.write(f"- **{nama_bersih}**: RM {harga_float:.2f}")
            total_harga += harga_float

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
          pilih = st.checkbox(
              f"{nama_addon} (+RM {harga_addon_float:.2f})",
              key=f"addon_row_{index}",
          )
          if pilih:
            total_harga += harga_addon_float
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
