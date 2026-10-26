import streamlit as st
import pandas as pd
import os

st.title("🚗 Sistem Pilihan Servis Kenderaan (Nizar Auto)")
st.write("Sila pilih model kenderaan dan servis tambahan pilihan anda di bawah:")

nama_fail_excel = "BASIC SERVICE NIZAR.xlsx"

if os.path.exists(nama_fail_excel):
    # Baca fail Excel dari Sheet pertama
    df = pd.read_excel(nama_fail_excel, sheet_name=0)
    
    # Senarai model kenderaan (selain kolum tertentu)
    model_list = [col for col in df.columns if col not in ['MODEL', 'ADDITIONAL SERVICE', 'PRICE']]
    
    # 1. Pelanggan pilih model kereta
    model_pilihan = st.selectbox("Pilih Model Kenderaan Anda:", model_list)
    
    total_harga = 0.0
    
    # --- BAHAGIAN 1: SERVIS ASAS ---
    st.subheader(f"📋 Senarai Servis Asas untuk: {model_pilihan}")
    
    for index, row in df.iterrows():
        item_servis = row['MODEL']
        
        # Hentikan gelung jika berjumpa baris kosong atau bahagian 'ADDITIONAL SERVICE'
        if pd.isna(item_servis) or str(item_servis).strip() == "" or "ADDITIONAL" in str(item_servis).upper():
            break
            
        harga = row[model_pilihan]
        
        # Abaikan baris SUBTOTAL asal
        if str(item_servis).strip().upper() != "SUBTOTAL":
            if pd.notna(harga):
                try:
                    harga_float = float(harga)
                    st.write(f"- **{item_servis}**: RM {harga_float:.2f}")
                    total_harga += harga_float
                except ValueError:
                    pass

    # --- BAHAGIAN 2: ADDITIONAL SERVICE (TAMBAHAN) ---
    st.subheader("🛠️ Servis Tambahan Pilihan (Optional)")
    
    if 'ADDITIONAL SERVICE' in df.columns and 'PRICE' in df.columns:
        add_on_df = df[['ADDITIONAL SERVICE', 'PRICE']].dropna(subset=['ADDITIONAL SERVICE'])
        
        for index, row in add_on_df.iterrows():
            nama_addon = row['ADDITIONAL SERVICE']
            harga_addon = row['PRICE']
            
            if pd.notna(nama_addon) and str(nama_addon).strip() != "" and pd.notna(harga_addon):
                try:
                    harga_addon_float = float(harga_addon)
                    pilih = st.checkbox(f"{nama_addon} (+RM {harga_addon_float:.2f})", key=f"addon_{index}")
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
        st.info("Sebut harga berjaya direkodkan! Sila tunjukkan skrin ini kepada Service Advisor.")

else:
    st.error(f"⚠️ Fail '{nama_fail_excel}' tidak dijumpai di dalam folder!")
