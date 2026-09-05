# panel.py

import streamlit as st
import json
import os
import pandas as pd
from openai import OpenAI

# --- KESİN ÇÖZÜM: DOSYALARIN MUTLAK YOLU (ABSOLUTE PATH) ---
# Linux sunucusunda Streamlit'in kör kalmaması için hedefleri tam adresiyle veriyoruz
SEKTOR_DOSYASI = "/mnt/c/Users/Hasan Doğan/sohbet/sektor_akisi.json"
GOLGE_DOSYASI = "/mnt/c/Users/Hasan Doğan/sohbet/golge_savas_raporu.json"
# //[EK] Dosya yolları Karargahın (WSL) ana istihbarat dizinine mühürlendi.

# --- 1. HAFIZA ODASINI (SESSION STATE) İLK AÇILIŞTA HAZIRLAMA ---
if "sektor_gecmisi" not in st.session_state:
    st.session_state.sektor_gecmisi = {
        "Ulaştırma-Havacılık": {"T_2": 0.0, "T_1": 0.0, "T_0": 0.0, "Toplam": 0.0},
        "Enerji-Elektrik":     {"T_2": 0.0, "T_1": 0.0, "T_0": 0.0, "Toplam": 0.0},
        "Otomotiv-Sanayi":    {"T_2": 0.0, "T_1": 0.0, "T_0": 0.0, "Toplam": 0.0},
        "Holding-İnşaat":     {"T_2": 0.0, "T_1": 0.0, "T_0": 0.0, "Toplam": 0.0},
        "Perakende-Gıda":     {"T_2": 0.0, "T_1": 0.0, "T_0": 0.0, "Toplam": 0.0},
        "Ağır-Sanayi":        {"T_2": 0.0, "T_1": 0.0, "T_0": 0.0, "Toplam": 0.0},
        "Telekomünikasyon":   {"T_2": 0.0, "T_1": 0.0, "T_0": 0.0, "Toplam": 0.0},
        "Teknoloji-Savunma":   {"T_2": 0.0, "T_1": 0.0, "T_0": 0.0, "Toplam": 0.0}
    }

if "son_okunan_veri" not in st.session_state:
    st.session_state.son_okunan_veri = {}


# --- 2. GİZLİ KÖPRÜDEN VERİ ÇEKME VE ZAMANI KAYDIRMA MOTORU ---
if os.path.exists(SEKTOR_DOSYASI):
    try:
        with open(SEKTOR_DOSYASI, "r", encoding="utf-8") as f:
            canli_disk_verisi = json.load(f)

        if canli_disk_verisi != st.session_state.son_okunan_veri:
            for sektor, anlik_hacim in canli_disk_verisi.items():
                if  sektor in st.session_state.sektor_gecmisi:
                    st.session_state.sektor_gecmisi[sektor]["T_2"] = st.session_state.sektor_gecmisi[sektor]["T_1"]
                    st.session_state.sektor_gecmisi[sektor]["T_1"] = st.session_state.sektor_gecmisi[sektor]["T_0"]
                    st.session_state.sektor_gecmisi[sektor]["T_0"] = float(anlik_hacim)
                    st.session_state.sektor_gecmisi[sektor]["Toplam"] += float(anlik_hacim)

            st.session_state.son_okunan_veri = canli_disk_verisi

    except Exception as e:
        st.error(f"Narin köprüde okuma sızısı oluştu: {str(e)}")


# --- 3. EĞİLİM VE MOMENTUMU HESAPLAYAN KURMAY MANTIĞI ---
def trend_durumunu_belirle(t2, t1, t0):
    if t0 == 0.0 and t1 == 0.0 and t2 == 0.0:
        return "⚪ Beklemede"

    if t0 > t1 and t1 > t2:
        return "⚡ Hızlanıyor (Artan Giriş)"
    elif t0 < t1 and t1 < t2:
        return "📉 Yavaşlıyor (Azalan Giriş)"
    else:
        return "⚪ Yatay Sürdürülebilir"


# --- SAYFA AYARLARI VE ANA BAŞLIK ---
st.set_page_config(page_title="GMN MATRIX KARARGAH", layout="wide", initial_sidebar_state="expanded")

# --- SOL KENAR KUMANDA PANOSU (SIDEBAR) ---
st.sidebar.title("🛡️ ANA MENÜ")
secim = st.sidebar.radio(
    "Giriş Yapılacak Karargah Odası:",
    ["🎙️ Subay Telsizi (Sohbet)", "📊 Otonom Karargah (Gözlem)"]
)
st.sidebar.markdown("---")
st.sidebar.info("Üst menü AYZERS ile strateji konuşmak içindir. Alt menü ise otonom filonun borsa tahtasındaki işlemlerini izlemek içindir.")

# ==========================================================
# 1. ODA: TELEFON UYUMLU YAPAY ZEKA TELSİZİ (SOHBET)
# ==========================================================
if secim == "🎙️ Subay Telsizi (Sohbet)":
    st.title("🎙️ Özel Yapay Zeka Risk Subayı (AYZERS)")

    # LM Studio Telsiz Bağlantısı
    LM_STUDIO_API_URL = "http://192.168.1.116:1234/v1"
    client = OpenAI(base_url=LM_STUDIO_API_URL, api_key="lm-studio")
    DOKTRIN_DOSYASI = "subay_doktrin.txt"

    # Oturum Hafızasını (Session State) Başlat
    if "mesajlar" not in st.session_state:
        try:
            with open(DOKTRIN_DOSYASI, "r", encoding="utf-8") as dosya:
                system_prompt = dosya.read()
        except FileNotFoundError:
            system_prompt = "Sen AYZERS Risk Subayısın."
            st.error(f"{DOKTRIN_DOSYASI} bulunamadı, subay kuralsız çalışıyor!")

        # Subayın beynine kazınan kurallar ve ekranda görünecek sohbet geçmişi
        st.session_state.mesajlar = [{"role": "system", "content": system_prompt}]
        st.session_state.gosterilecek_mesajlar = []

    # Geçmiş sohbetleri telefon ekranına çiz
    for msg in st.session_state.gosterilecek_mesajlar:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Klavyeden veya telefondan yeni mesaj girişi
# Klavyeden veya telefondan yeni mesaj girişi
    if prompt := st.chat_input("Mareşal, emriniz nedir?"):
        # Kullanıcının yazdığını ekrana ekle
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.mesajlar.append({"role": "user", "content": prompt})
        st.session_state.gosterilecek_mesajlar.append({"role": "user", "content": prompt})

        # [EK] RADAR: Sizin mesajınızı siyah terminale basar
        print(f"=========================================")
        print(f"📲 [DIŞ TELSİZ] Gelen Mesaj: {prompt}")

        # Subayın cevabını LM Studio'dan bekle ve ekrana yaz
        with st.chat_message("assistant"):
            mesaj_alani = st.empty()
            mesaj_alani.markdown("Subay Düşünüyor...")
            try:
                response = client.chat.completions.create(
                    model="ayzers",
                    messages=st.session_state.mesajlar,
                    temperature=0.1
                )
                subay_cevabi = response.choices[0].message.content
                mesaj_alani.markdown(subay_cevabi)

                st.session_state.mesajlar.append({"role": "assistant", "content": subay_cevabi})
                st.session_state.gosterilecek_mesajlar.append({"role": "assistant", "content": subay_cevabi})

                # [EK] RADAR: Subayın cevabını siyah terminale basar
                print(f"🤖 [AYZERS CEVABI]: {subay_cevabi}")
                print(f"=========================================\n")

            except Exception as e:
                mesaj_alani.error(f"Bağlantı Hatası: Karargah motoru (LM Studio) yanıt vermiyor. Detay: {e}")
               
# ==========================================================
# 2. ODA: OTONOM FİLO GÖZLEM KULESİ (MEVCUT PANELİNİZ)
# ==========================================================
elif secim == "📊 Otonom Karargah (Gözlem)":
    st.title("📊 Otonom Karargah Gözlem Paneli")
    st.markdown("### 🎯 Hedef: Borsa İstanbul (BIST) 40 Hisse Eşzamanlı Operasyonu")

    sekme_tatbikat, sekme_rotasyon = st.tabs(["🛡️ Gölge Tatbikat ve İrfan Merkezi", "📡 Canlı Sektör Rotasyonu"])

    # ====================================================================
    # --- 1. ODANIN İÇİ: GÖLGE TATBİKAT VE PERFORMANS MERKEZİ ---
    # ====================================================================
    with sekme_tatbikat:
        gecmis_islemler = []

        if os.path.exists(GOLGE_DOSYASI):
            with open(GOLGE_DOSYASI, "r", encoding="utf-8") as f:
                for satir in f:
                    if satir.strip():
                        try:
                            gecmis_islemler.append(json.loads(satir))
                        except:
                            pass

        if gecmis_islemler:
            df_islemler = pd.DataFrame(gecmis_islemler)
            toplam_islem = len(df_islemler)
            basarili_islemler = df_islemler[df_islemler['pnl'] > 0]
            win_rate = (len(basarili_islemler) / toplam_islem) * 100 if toplam_islem > 0 else 0.0
            toplam_pnl = df_islemler['pnl'].sum()
            son_kasa = df_islemler['yeni_bakiye'].iloc[-1] if 'yeni_bakiye' in df_islemler.columns else 100000.0

            m1, m2, m3, m4 = st.columns(4)
            m1.metric(label="Toplam Tatbikat", value=f"{toplam_islem} İşlem")
            m2.metric(label="Başarı Oranı (Win Rate)", value=f"%{win_rate:.1f}")
            m3.metric(label="Net Kâr/Zarar (PnL)", value=f"{toplam_pnl:.2f} ₺")
            m4.metric(label="Son Kasa Durumu", value=f"{son_kasa:.2f} ₺")

            st.write("---")
            st.subheader("📈 Birlik Performansları ve PnL Eğrisi")
            if "yeni_bakiye" in df_islemler.columns:
                st.line_chart(df_islemler[["yeni_bakiye"]], width="stretch")

            st.write("---")
            st.subheader("📝 Gölge Defter İşlem Geçmişi (Gerçek Zamanlı)")

            def pnl_renklendir(deger):
                try:
                    if float(deger) > 0:
                        return 'color: #00FF00; font-weight: bold;'
                    elif float(deger) < 0:
                        return 'color: #FF0000; font-weight: bold;'
                    return 'color: gray;'
                except:
                    return ''

            if hasattr(df_islemler.style, 'map'):
                styled_df = df_islemler.style.map(pnl_renklendir, subset=['pnl'])
            else:
                styled_df = df_islemler.style.applymap(pnl_renklendir, subset=['pnl'])

            st.dataframe(styled_df, width="stretch")
        else:
            st.info("Sükûnet hâkim... Henüz gölge deftere nakşedilmiş kapanmış bir sanal muharebe bulunmuyor.")


    # ====================================================================
    # --- 2. ODANIN İÇİ: CANLI SEKTÖR ROTASYONU ---
    # ====================================================================
    with sekme_rotasyon:
        # Canlı veriyi anında tarayıcıya yansıtmak için şefkatli bir buton
        if st.button("🔄 Radarı Yenile (Taze Verileri Çek)"):
            st.rerun()

        st.subheader("📋 Radardaki Sektörlerin Zaman-Hacim Matrisi")
        tablo_datasi = []

        for sektor, veriler in st.session_state.sektor_gecmisi.items():
            trend = trend_durumunu_belirle(veriler["T_2"], veriler["T_1"], veriler["T_0"])

            tablo_datasi.append({
                "Sektör Adı": sektor,
                "10-15 Dk Önce (₺)": f"{veriler['T_2']:,.2f}",
                "5-10 Dk Önce (₺)":  f"{veriler['T_1']:,.2f}",
                "Son 5 Dakika (₺)":  f"{veriler['T_0']:,.2f}",
                "Toplam Hacim (₺)":  f"{veriler['Toplam']:,.2f}",
                "Akış Eğilimi (Trend)": trend
            })

        df_tablo = pd.DataFrame(tablo_datasi)
        st.table(df_tablo)

        st.write("---")
        st.subheader("📊 Son 5 Dakikalık Canlı Hacim Momentum İvmesi")

        grafik_sozlugu = {
            "Sektörler": list(st.session_state.sektor_gecmisi.keys()),
            "Nakit Gücü (TL)": [veriler["T_0"] for veriler in st.session_state.sektor_gecmisi.values()]
        }
        df_grafik = pd.DataFrame(grafik_sozlugu).set_index("Sektörler")
        st.bar_chart(df_grafik, width="stretch")
# //[EK] Karargah Onaylı. Görselleştirme modülleri kusursuz çalışıyor.
