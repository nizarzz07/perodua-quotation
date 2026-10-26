import streamlit as st
import pandas as pd
import os

st.title("🚗 Sistem Pilihan Servis Kenderaan (Service Advisor Nizar)")
st.write("Sila pilih model kenderaan dan keperluan servis anda di bawah:")

nama_fail_excel = "BASIC SERVICE NIZAR.xlsx"

if os.path.exists(nama_fail_excel):
    # Baca fail Excel dari Sheet pertama
    df = pd.read_excel(nama_fail_excel, sheet_name=0)
    
    # Senarai model kenderaan adalah tajuk kolum (selain kolum pertama 'MODEL')
    model_list = [col for col in df.columns if col != 'MODEL']
    
    # 1. Pelanggan pilih model kereta
    model_pilihan = st.selectbox("Pilih Model Kenderaan Anda:", model_list)
    
    st.subheader(f"📋 Senarai Servis Asas untuk: {model_pilihan}")
    
    total_harga = 0.0
    
    # Paparkan item dan harga mengikut model yang dipilih
    for index, row in df.iterrows():
        item_servis = row['MODEL']
        harga = row[model_pilihan]
        
        # Abaikan baris SUBTOTAL dari Excel kerana kita akan kira secara automatik
        if str(item_servis).strip().upper() != "SUBTOTAL":
            if pd.notna(harga):
                st.write(f"- **{item_servis}**: RM {float(harga):.2f}")
                total_harga += float(harga)

    # 2. Paparan Keputusan Jumlah Keseluruhan
    st.markdown("---")
    st.subheader("💰 Anggaran Jumlah Keseluruhan (Grand Total)")
    st.success(f"**RM {total_harga:.2f}**")

    if st.button("Cetak / Sahkan Sebut Harga"):
        st.balloons()
        st.info("Sebut harga berjaya direkodkan! Sila tunjukkan skrin ini kepada Service Advisor.")

else:
    st.error(f"⚠️ Fail '{nama_fail_excel}' tidak dijumpai di dalam folder! Sila pastikan fail Excel berada di dalam folder Python yang sama.")





    
