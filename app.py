# Senarai item yang boleh dipilih atau ditolak (lalai = False / tidak dipilih)
    optional_items = ["INJECTOR CLEANER", "WINDSHIELD WASHER FLUID", "JAS WSSF"]
    
    for index, row in df.iterrows():
        item_servis = row['MODEL']
        
        if pd.isna(item_servis) or str(item_servis).strip() == "" or "ADDITIONAL" in str(item_servis).upper():
            break
            
        harga = row[model_pilihan]
        nama_bersih = str(item_servis).replace("*", "").strip()
        
        if nama_bersih.upper() != "SUBTOTAL":
            if pd.notna(harga):
                try:
                    harga_float = float(harga)
                    
                    # Jika item optional, jadikan checkbox dengan nilai lalai False (tidak dipilih)
                    if any(opt in nama_bersih.upper() for opt in optional_items):
                        pilih_item = st.checkbox(f"{nama_bersih} (+RM {harga_float:.2f})", value=False, key=f"opt_item_{index}")
                        if pilih_item:
                            total_harga += harga_float
                    else:
                        # Servis wajib kekal dimasukkan terus
                        st.write(f"- **{nama_bersih}**: RM {harga_float:.2f}")
                        total_harga += harga_float
                        
                except ValueError:
                    pass
