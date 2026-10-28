import datetime
import os
import pandas as pd
import streamlit as st

# 1. Tetapan Halaman
st.set_page_config(
    page_title="Perodua Sarinani Motors - Quotation",
    page_icon="🚗",
    layout="centered",
)

# Kamus Terjemahan untuk 3 Bahasa (Slot Masa Bermula 8:30 Pagi hingga 4:00 Petang)
translations = {
    "Malay": {
        "title": "Sistem Pilihan Servis Kenderaan",
        "subtitle": "Perodua Sarinani Motors Sdn Bhd • Rasmi & Profesional",
        "customer_info": "👤 Maklumat Pelanggan & Temujanji Kalendar",
        "name_label": "Nama Pelanggan:",
        "plate_label": "No. Pendaftaran Kenderaan (No. Plat):",
        "date_label": "Pilih Tarikh Temujanji (Isnin - Sabtu):",
        "time_label": "Pilih Slot Masa Temujanji:",
        "select_model": "Pilih Model Kenderaan Anda:",
        "basic_service": "📋 Senarai Servis Asas",
        "additional_service": "🛠️ Servis Tambahan Pilihan (Optional)",
        "est_time": "⏱️ Anggaran Masa Siap Servis di Bengkel:",
        "time_value": "Anggaran 2 - 3 Jam (Bergantung pada jenis servis & keadaan bengkel)",
        "grand_total": "ANGGARAN KESELURUHAN (GRAND TOTAL)",
        "whatsapp_btn": "📱 Hantar ke WhatsApp Service Advisor",
        "whatsapp_msg": (
            "Hai Service Advisor Sarinani Motors,%0ASaya ingin membuat temujanji"
            " servis dengan butiran berikut:%0A• Nama: *{name}*%0A• No. Plat:"
            " *{plate}*%0A• Tarikh: *{date} ({day})*%0A• Slot Masa:"
            " *{time}*%0A• Model: *{model}*%0A• Anggaran Jumlah: *RM"
            " {total}*%0AMohon sahkan slot temujanji saya."
        ),
        "error_sunday": (
            "⚠️ Maaf, pusat servis kami tutup pada hari Ahad. Sila pilih"
            " tarikh dari hari Isnin hingga Sabtu."
        ),
        "jas_wssf_desc": (
            "• **JAS**: Pelaksanaan Caj Pelupusan Sisa Berjadual"
            " (Environment Waste Fee) minimum sebanyak RM5.00.\n• **WSSF**:"
            " Pelaksanaan Caj Bahan Consumable dan Sanitasi Bengkel."
        ),
        "ozone_desc": (
            "Rawatan ozon untuk membunuh bakteria, kulat, dan menyahbau"
            " kurang menyenangkan di dalam kabin kereta."
        ),
        "times": [
            "08:30 Pagi",
            "09:00 Pagi",
            "09:30 Pagi",
            "10:00 Pagi",
            "10:30 Pagi",
            "11:00 Pagi",
            "11:30 Pagi",
            "12:00 Tengah Hari",
            "12:30 Tengah Hari",
            "01:00 Petang",
            "01:30 Petang",
            "02:00 Petang",
            "02:30 Petang",
            "03:00 Petang",
            "03:30 Petang",
            "04:00 Petang",
        ],
        "day_names": [
            "Isnin",
            "Selasa",
            "Rabu",
            "Khamis",
            "Jumaat",
            "Sabtu",
            "Ahad",
        ],
    },
    "English": {
        "title": "Vehicle Service Selection System",
        "subtitle": "Perodua Sarinani Motors Sdn Bhd • Official & Professional",
        "customer_info": "👤 Customer & Calendar Appointment Information",
        "name_label": "Customer Name:",
        "plate_label": "Vehicle Registration Number (Plate No.):",
        "date_label": "Select Appointment Date (Monday - Saturday):",
        "time_label": "Select Appointment Time Slot:",
        "select_model": "Select Your Vehicle Model:",
        "basic_service": "📋 Basic Service List",
        "additional_service": "🛠️ Optional Additional Services",
        "est_time": "⏱️ Estimated Workshop Service Duration:",
        "time_value": (
            "Approx. 2 - 3 Hours (Subject to service type & workshop load)"
        ),
        "grand_total": "GRAND TOTAL ESTIMATE",
        "whatsapp_btn": "📱 Send to WhatsApp Service Advisor",
        "whatsapp_msg": (
            "Hi Service Advisor Sarinani Motors,%0AI would like to book a"
            " service appointment with the following details:%0A• Name:"
            " *{name}*%0A• Plate No.: *{plate}*%0A• Date: *{date} ({day})*%0A•"
            " Time Slot: *{time}*%0A• Model: *{model}*%0A• Estimated Total: *RM"
            " {total}*%0APlease confirm my appointment slot."
        ),
        "error_sunday": (
            "⚠️ Sorry, our service center is closed on Sundays. Please choose"
            " a date from Monday to Saturday."
        ),
        "jas_wssf_desc": (
            "• **JAS**: Scheduled Waste Disposal Fee (Environment Waste Fee)"
            " minimum of RM5.00.\n• **WSSF**: Workshop Consumables and"
            " Sanitation Fee."
        ),
        "ozone_desc": (
            "Ozone treatment to kill bacteria, fungi, and eliminate unpleasant"
            " odors in the car cabin."
        ),
        "times": [
            "08:30 AM",
            "09:00 AM",
            "09:30 AM",
            "10:00 AM",
            "10:30 AM",
            "11:00 AM",
            "11:30 AM",
            "12:00 PM",
            "12:30 PM",
            "01:00 PM",
            "01:30 PM",
            "02:00 PM",
            "02:30 PM",
            "03:00 PM",
            "03:30 PM",
            "04:00 PM",
        ],
        "day_names": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
    },
    "Chinese": {
        "title": "车辆保养选择系统",
        "subtitle": "Perodua Sarinani Motors Sdn Bhd • 官方与专业",
        "customer_info": "👤 客户与日历预约信息",
        "name_label": "客户姓名：",
        "plate_label": "车牌号码：",
        "date_label": "选择预约日期（周一至周六）：",
        "time_label": "选择预约时间段：",
        "select_model": "请选择您的车辆型号：",
        "basic_service": "📋 基本保养清单",
        "additional_service": "🛠️ 可选附加服务",
        "est_time": "⏱️ 预计车间保养所需时间：",
        "time_value": "大约 2 - 3 小时（视保养类型及车间情况而定）",
        "grand_total": "预估总费用 (GRAND TOTAL)",
        "whatsapp_btn": "📱 发送至 WhatsApp 服务顾问",
        "whatsapp_msg": (
            "您好 Sarinani Motors 服务顾问，%0AI 想预约保养，详情如下：%0A• 姓名：*{name}*%0A•"
            " 车牌：*{plate}*%0A• 日期：*{date} ({day})*%0A• 时间段：*{time}*%0A•"
            " 型号：*{model}*%0A• 预估总额： *RM {total}*%0A请帮我确认预约时段。"
        ),
        "error_sunday": (
            "⚠️ 对不起，我们的服务中心周日休息。请选择周一至周六之间的日期。"
        ),
        "jas_wssf_desc": (
            "• **JAS**: 定期废物处理费（环境废物费）最低 RM5.00。\n• **WSSF**:"
            " 车间耗材及消毒费。"
        ),
        "ozone_desc": "臭氧杀菌处理，可杀灭细菌、真菌并消除车厢内的异味。",
        "times": [
            "上午 08:30",
            "上午 09:00",
            "上午 09:30",
            "上午 10:00",
            "上午 10:30",
            "上午 11:00",
            "上午 11:30",
            "中午 12:00",
            "中午 12:30",
            "下午 01:00",
            "下午 01:30",
            "下午 02:00",
            "下午 02:30",
            "下午 03:00",
            "下午 03:30",
            "下午 04:00",
        ],
        "day_names": [
            "星期一",
            "星期二",
            "星期三",
            "星期四",
            "星期五",
            "星期六",
            "星期日",
        ],
    },
}

# 2. CSS Kustom untuk Tema Cerah & Kalendar
st.markdown(
    """
    <style>
        .stApp {
            background-color: #FFFFFF !important;
            color: #1a1a1a !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        div[data-baseweb="select"] > div, input[type="text"], input[type="date"] {
            background-color: #f9f9f9 !important;
            color: #1a1a1a !important;
            border: 1px solid #ccc !important;
        }

        div[data-baseweb="popover"] div, ul[data-baseweb="menu"] {
            background-color: #FFFFFF !important;
            color: #1a1a1a !important;
        }

        li[data-baseweb="option"] div {
            color: #1a1a1a !important;
        }

        .perodua-header-card {
            background: linear-gradient(135deg, #f9f9f9 0%, #f1f1f1 100%);
            border: 2px solid #D71921;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }
        
        .perodua-header-card h1 {
            color: #D71921;
            font-size: 22px;
            margin: 10px 0 5px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .perodua-header-card p {
            color: #555555;
            font-size: 13px;
            margin: 0;
        }

        .info-card {
            background-color: #fafafa;
            border: 1px solid #e0e0e0;
            border-left: 5px solid #D71921;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .section-heading {
            font-size: 18px;
            color: #D71921;
            border-bottom: 2px solid #D71921;
            padding-bottom: 5px;
            margin-top: 25px;
            margin-bottom: 15px;
            font-weight: bold;
        }

        .grand-total-box {
            background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
            border: 2px solid #D71921;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-top: 25px;
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

        p, span, label, div {
            color: #1a1a1a;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Pilihan Bahasa
selected_lang = st.selectbox(
    "🌐 Choose Language / Pilih Bahasa / 选择语言:", ["Malay", "English", "Chinese"]
)
t = translations[selected_lang]

# 3. PAPARAN LOGO & KOTAK TAJUK
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  if os.path.exists("sarinani_motors_logo.png"):
    st.image("sarinani_motors_logo.png", use_container_width=True)
  elif os.path.exists("Perodua-Logo.png"):
    st.image("Perodua-Logo.png", use_container_width=True)

st.markdown(
    f"""
    <div class="perodua-header-card">
        <h1>{t["title"]}</h1>
        <p>{t["subtitle"]}</p>
    </div>
    """,
    unsafe_allow_html=True,
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

  # --- MAKLUMAT PELANGGAN & KALENDAR TEMUJANJI ---
  st.markdown(f"### {t['customer_info']}")
  nama_pelanggan = st.text_input(t["name_label"], placeholder="cth: En. Ahmad")
  no_plat = st.text_input(t["plate_label"], placeholder="cth: VAB 1234")

  col_date, col_time = st.columns(2)
  with col_date:
    pilihan_tarikh = st.date_input(
        t["date_label"], value=datetime.date.today()
    )
  with col_time:
    pilihan_masa = st.selectbox(t["time_label"], t["times"])

  # Semak jika hari Ahad
  is_sunday = pilihan_tarikh.weekday() == 6

  if is_sunday:
    st.error(t["error_sunday"])
  else:
    nama_hari = t["day_names"][pilihan_tarikh.weekday()]
    model_pilihan = st.selectbox(t["select_model"], model_list)
    total_harga = 0.0

    # --- BAHAGIAN 1: SERVIS ASAS ---
    st.markdown(
        f'<div class="section-heading">{t["basic_service"]}</div>',
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

            col_a, col_b = st.columns([3, 1])
            with col_a:
              st.write(f"• **{nama_bersih}**")
            with col_b:
              st.write(f"**RM {harga_float:.2f}**")

            if "JAS WSSF" in nama_bersih.upper():
              with st.expander(f"ℹ️ Info / 详情: {nama_bersih}"):
                st.write(t["jas_wssf_desc"])

          except ValueError:
            pass

    # --- BAHAGIAN 2: SERVIS TAMBAHAN ---
    st.markdown(
        f'<div class="section-heading">{t["additional_service"]}</div>',
        unsafe_allow_html=True,
    )

    is_addon_section = False
    for index, row in df.iterrows():
      item_servis = str(row["MODEL"]).strip()

      if "ADDITIONAL" in item_servis.upper():
        is_addon_section = True
        continue

      if is_addon_section and pd.notna(row["MODEL"]) and row["MODEL"] != "":
        nama_addon = (
            str(row["MODEL"]).replace("*", "").strip()
            if pd.notna(row["MODEL"])
            else ""
        )
        harga_addon = row[df.columns[1]]

        if pd.notna(harga_addon) and str(harga_addon).strip() != "":
          try:
            harga_addon_float = float(harga_addon)

            pilih = st.checkbox(
                f"Tambah / Add **{nama_addon}** (+RM {harga_addon_float:.2f})",
                key=f"addon_row_{index}",
            )
            if pilih:
              total_harga += harga_addon_float

            if "OZONE" in nama_addon.upper():
              with st.expander(f"ℹ️ Info / 详情: {nama_addon}"):
                st.write(t["ozone_desc"])

          except ValueError:
            pass

    # --- ANGGARAN MASA SIAP ---
    st.markdown(
        f"""
        <div class="info-card">
            <b>{t['est_time']}</b><br>
            <span style="color: #D71921; font-weight: bold;">{t['time_value']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- BAHAGIAN 3: JUMLAH KESELURUHAN ---
    st.markdown(
        f"""
        <div class="grand-total-box">
            <div class="grand-total-title">{t["grand_total"]}</div>
            <div class="grand-total-price">RM {total_harga:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    final_nama = nama_pelanggan if nama_pelanggan else "Tidak Diisi"
    final_plat = no_plat if no_plat else "Tidak Diisi"
    formatted_date = pilihan_tarikh.strftime("%d/%m/%Y")

    pesanan_wa = t["whatsapp_msg"].format(
        name=final_nama,
        plate=final_plat,
        date=formatted_date,
        day=nama_hari,
        time=pilihan_masa,
        model=model_pilihan,
        total=f"{total_harga:.2f}",
    )
    pautan_wa = f"https://wa.me/?text={pesanan_wa}"

    st.markdown(
        f"""
        <a href="{pautan_wa}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366; color:white; padding:14px; border-radius:8px; text-align:center; font-weight:bold; font-size:16px; box-shadow: 0 4px 10px rgba(37, 211, 102, 0.2);">
                {t["whatsapp_btn"]}
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )

else:
  st.error(f"Fail '{nama_fail_excel}' tidak dijumpai di dalam folder!")
