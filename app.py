import streamlit as st
import pandas as pd
import os

st.title("🚗 Sistem Pilihan Servis Kenderaan (Nizar Auto)")
st.write("Sila pilih model kenderaan dan servis tambahan pilihan anda di bawah:")

nama_fail_excel = "BASIC SERVICE NIZAR.xlsx"

if os.path.exists(nama_fail_excel):
    # Baca fail Excel dari Sheet pertama
    df = pd.read_excel(nama_fail_excel, sheet_name=0)
    
    # Senarai model kenderaan (selain kolum 'MODEL')
    model_list = [col for col in df.columns if col not in ['MODEL', 'ADDITIONAL SERVICE', 'PRICE']]
    
    # 1. Pelanggan pilih model kereta
    model_pilihan = st.selectbox("Pilih Model Kenderaan Anda:", model_list)
    
    total_harga = 0.0
    
    # --- BAHAGIAN 1: SERVIS ASAS ---
    st.subheader(f"📋 Senarai Servis Asas untuk: {model_pilihan}")
    
    for index, row in df.iterrows():
        item_servis = row['MODEL']
        harga = row[model_pilihan]
        
        # Pastikan ia bukan baris kosong atau SUBTOTAL
        if pd.notna(item_servis) and str(item_servis).strip().upper() != "SUBTOTAL":
            if pd.notna(harga):
                st.write(f"- **{item_servis}**: RM {float(harga):.2f}")
                total_harga += float(harga)

    # --- BAHAGIAN 2: ADDITIONAL SERVICE (TAMBAHAN) ---
    st.subheader("🛠️ Servis Tambahan Pilihan (Optional)")
    
    # Semak jika kolum 'ADDITIONAL SERVICE' wujud dalam excel
    if 'ADDITIONAL SERVICE' in df.columns and 'PRICE' in df.columns:
        add_on_df = df[['ADDITIONAL SERVICE', 'PRICE']].dropna(subset=['ADDITIONAL SERVICE'])
        
        selected_addons = []
        for index, row in add_on_df.iterrows():
            nama_addon = row['ADDITIONAL SERVICE']
            harga_addon = row['PRICE']
            
            if pd.notna(nama_addon) and pd.notna(harga_addon):
                # Buat checkbox untuk setiap additional service
                pilih = st.checkbox(f"{nama_addon} (+RM {float(harga_addon):.2f})", key=f"addon_{index}")
                if pilih:
                    total_harga += float(harga_addon)

    # 3. Paparan Jumlah Keseluruhan
    st.markdown("---")
    st.subheader("💰 Anggaran Jumlah Keseluruhan (Grand Total)")
    st.success(f"**RM {total_harga:.2f}**")

    if st.button("Cetak / Sahkan Sebut Harga"):
        st.balloons()
        st.info("Sebut harga berjaya direkodkan! Sila tunjukkan skrin ini kepada Service Advisor.")

else:
    st.error(f"⚠️ Fail '{nama_fail_excel}' tidak dijumpai di dalam folder!")
    
