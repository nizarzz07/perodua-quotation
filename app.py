import os
import pandas as pd
import streamlit as st

# 1. Tetapan Halaman
st.set_page_config(
    page_title="Perodua Sarinani Motors - Quotation",
    page_icon="🚗",
    layout="centered",
)

# 2. Hiasan Muka Depan (Interface CSS & HTML - Tema Putih & Hitam)
st.markdown(
    """
    <style>
        /* Tetapan latar belakang utama kepada Putih dan teks Hitam */
        .stApp {
            background-color: #FFFFFF;
            color: #1a1a1a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Kotak Hiasan Header */
        .perodua-header-card {
            background: linear-gradient(135deg, #f9f9f9 0%, #f1f1f1 100%);
            border: 2px solid #D71921;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            margin-bottom: 25px;
        }
        
        .perodua-header-card h1 {
            color: #D71921;
            font-size: 24px;
            margin: 10px 0 5px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .perodua-header-card p {
            color: #555555;
            font-size: 14px;
            margin: 0;
        }

        /* Seksyen Tajuk Kecil */
        .section-heading {
            font-size: 18px;
            color: #D71921;
            border-bottom: 2px solid #D71921;
            padding-bottom: 5px;
            margin-top: 25px;
            margin-bottom: 15px;
            font-weight: bold;
        }

        /* Kad Jumlah Keseluruhan (Grand Total) */
        .grand-total-box {
            background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
            border: 2px solid #D71921;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-top: 30px;
            box-shadow: 0 4px 15px rgba(215, 25, 33, 0.15);
        }
        
        .grand-total-title {
            color: #555555;
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 1px;
            margin: 0;
        }
        
        .grand-total-price {
            font-size: 32px;
            color: #D71921;
            font-weight: bold;
            margin-top: 5px;
        }

        /* Paksa teks dalam Streamlit jadi hitam */
        p, span, label, div {
            color: #1a1a1a;
        }
    </style>
    
    <div class="perodua-header-card">
        <h1>Sistem Pilihan Servis Kenderaan</h1>
        <p>Perodua Sarinani Motors Sdn Bhd • Rasmi & Profesional</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 3. Paparan Logo Rasmi
if os.path.exists("sarinani_motors_logo.png"):
  st.image("sarinani_motors_logo.png", use_container_width=True)
elif os.path.exists("Perodua-Logo.png"):
  st.image("Perodua-Logo.png", use_container_width=True)

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

  # Pilihan Model Kenderaan
  model_pilihan = st.selectbox("Pilih Model Kenderaan Anda:", model_list)

  total_harga = 0.0

  # --- BAHAGIAN 1: SERVIS ASAS ---
  st.markdown(
      '<div class="section-heading">📋 Senarai Servis Asas</div>',
      unsafe_allow_html=True,
  )

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

          # Penerangan khas JAS WSSF
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

  # --- BAHAGIAN 2: SERVIS TAMBAHAN (ADDITIONAL) ---
  st.markdown(
      '<div class="section-heading">🛠️ Servis Tambahan Pilihan (Optional)</div>',
      unsafe_allow_html=True,
  )

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

          # Penerangan khas OZONE TREATMENT
          if "OZONE" in nama_addon.upper():
            with st.expander(f"ℹ️ Ketik untuk lihat penerangan: {nama_addon}"):
              st.write(
                  "Rawatan ozon untuk membunuh bakteria, kulat, dan menyahbau"
                  " kurang menyenangkan di dalam kabin kereta."
              )

        except ValueError:
          pass

  # --- BAHAGIAN 3: KOTAK JUMLAH KESELURUHAN (GRAND TOTAL) ---
  st.markdown(
      f"""
      <div class="grand-total-box">
          <div class="grand-total-title">ANGGARAN KESELURUHAN (GRAND TOTAL)</div>
          <div class="grand-total-price">RM {total_harga:.2f}</div>
      </div>
      """,
      unsafe_allow_html=True,
  )

  # Butang Tindakan (WhatsApp & Cetak)
  pesanan_wa = (
      f"Hai Service Advisor Sarinani Motors,%0ASaya berminat dengan sebut"
      f" harga bagi model *{model_pilihan}*%0AAnggaran Jumlah:"
      f" *RM {total_harga:.2f}*%0AMohon sahkan slot temujanji servis saya."
  )
  pautan_wa = f"https://wa.me/?text={pesanan_wa}"

  col_btn1, col_btn2 = st.columns(2)
  with col_btn1:
    if st.button("🎈 Sahkan Sebut Harga", use_container_width=True):
      st.balloons()
      st.info(
          "Sebut harga berjaya direkodkan! Sila tunjukkan skrin ini kepada"
          " Service Advisor."
      )

  with col_btn2:
    st.markdown(
        f"""
        <a href="{pautan_wa}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold; margin-top:2px;">
                📱 Hantar ke WhatsApp SA
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )

else:
  st.error(f"Fail '{nama_fail_excel}' tidak dijumpai di dalam folder!")import os
import pandas as pd
import streamlit as st

# 1. Tetapan Halaman
st.set_page_config(
    page_title="Perodua Sarinani Motors - Quotation",
    page_icon="🚗",
    layout="centered",
)

# 2. Hiasan Muka Depan (Interface CSS & HTML Template)
st.markdown(
    """
    <style>
        /* Tetapan latar belakang utama */
        .stApp {
            background-color: #121212;
            color: #f4f4f4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Kotak Hiasan Tema Hitam-Merah */
        .perodua-header-card {
            background: linear-gradient(135deg, #1a1a1a 0%, #2b0d0e 100%);
            border: 2px solid #D71921;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(215, 25, 33, 0.3);
            margin-bottom: 25px;
        }
        
        .perodua-header-card h1 {
            color: #D71921;
            font-size: 24px;
            margin: 10px 0 5px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .perodua-header-card p {
            color: #aaaaaa;
            font-size: 14px;
            margin: 0;
        }

        /* Seksyen Tajuk Kecil */
        .section-heading {
            font-size: 18px;
            color: #D71921;
            border-bottom: 2px solid #D71921;
            padding-bottom: 5px;
            margin-top: 25px;
            margin-bottom: 15px;
            font-weight: bold;
        }

        /* Kad Jumlah Keseluruhan (Grand Total) */
        .grand-total-box {
            background: linear-gradient(135deg, #2a080a 0%, #1a1a1a 100%);
            border: 2px solid #D71921;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-top: 30px;
            box-shadow: 0 4px 15px rgba(215, 25, 33, 0.4);
        }
        
        .grand-total-title {
            color: #aaaaaa;
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 1px;
            margin: 0;
        }
        
        .grand-total-price {
            font-size: 32px;
            color: #ffffff;
            font-weight: bold;
            margin-top: 5px;
        }
    </style>
    
    <div class="perodua-header-card">
        <h1>Sistem Pilihan Servis Kenderaan</h1>
        <p>Perodua Sarinani Motors Sdn Bhd • Rasmi & Profesional</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 3. Paparan Logo Rasmi
if os.path.exists("sarinani_motors_logo.png"):
  st.image("sarinani_motors_logo.png", use_container_width=True)
elif os.path.exists("Perodua-Logo.png"):
  st.image("Perodua-Logo.png", use_container_width=True)

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

  # Pilihan Model Kenderaan
  model_pilihan = st.selectbox("Pilih Model Kenderaan Anda:", model_list)

  total_harga = 0.0

  # --- BAHAGIAN 1: SERVIS ASAS ---
  st.markdown(
      '<div class="section-heading">📋 Senarai Servis Asas</div>',
      unsafe_allow_html=True,
  )

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

          # Penerangan khas JAS WSSF
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

  # --- BAHAGIAN 2: SERVIS TAMBAHAN (ADDITIONAL) ---
  st.markdown(
      '<div class="section-heading">🛠️ Servis Tambahan Pilihan (Optional)</div>',
      unsafe_allow_html=True,
  )

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

          # Penerangan khas OZONE TREATMENT
          if "OZONE" in nama_addon.upper():
            with st.expander(f"ℹ️ Ketik untuk lihat penerangan: {nama_addon}"):
              st.write(
                  "Rawatan ozon untuk membunuh bakteria, kulat, dan menyahbau"
                  " kurang menyenangkan di dalam kabin kereta."
              )

        except ValueError:
          pass

  # --- BAHAGIAN 3: KOTAK JUMLAH KESELURUHAN (GRAND TOTAL) ---
  st.markdown(
      f"""
      <div class="grand-total-box">
          <div class="grand-total-title">ANGGARAN KESELURUHAN (GRAND TOTAL)</div>
          <div class="grand-total-price">RM {total_harga:.2f}</div>
      </div>
      """,
      unsafe_allow_html=True,
  )

  # Butang Tindakan (WhatsApp & Cetak)
  pesanan_wa = (
      f"Hai Service Advisor Sarinani Motors,%0ASaya berminat dengan sebut"
      f" harga bagi model *{model_pilihan}*%0AAnggaran Jumlah:"
      f" *RM {total_harga:.2f}*%0AMohon sahkan slot temujanji servis saya."
  )
  pautan_wa = f"https://wa.me/?text={pesanan_wa}"

  col_btn1, col_btn2 = st.columns(2)
  with col_btn1:
    if st.button("🎈 Sahkan Sebut Harga", use_container_width=True):
      st.balloons()
      st.info(
          "Sebut harga berjaya direkodkan! Sila tunjukkan skrin ini kepada"
          " Service Advisor."
      )

  with col_btn2:
    st.markdown(
        f"""
        <a href="{pautan_wa}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold; margin-top:2px;">
                📱 Hantar ke WhatsApp SA
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )

else:
  st.error(f"Fail '{nama_fail_excel}' tidak dijumpai di dalam folder!")
