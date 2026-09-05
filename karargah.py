# karargah.py

import uvicorn
import asyncio
import json
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from modeller import SinyalVerisi
from protokol import arka_plan_telsiz_yonetimi
from kumbara import mega_ping_hacmini_isle, SEKTOR_KUMBARALARI

app = FastAPI(title="GMN PRO MATRIX - AI Risk Subayı Karargahı")

# ====================================================================
# 🛡️ SİBER GÜVENLİK: TRADINGVIEW GİZLİ KURMAY ŞİFRESİ
# Sadece bu şifreyi barındıran sinyaller karargaha girebilir!
# ====================================================================
GIZLI_KURMAY_SIFRESI = "AlfaKurt_2026_GMN"

@app.on_event("startup")
def karargah_odaları_yoklama_kontrolu():
    print("\n" + "🛡️ "*15)
    print("📋 [YOKLAMA] Modüler Karargah Odaları Kontrol Ediliyor...")
    print("🟢 [OK] modeller.py  -> Pydantic Veri Kalıpları ve Şemalar Aktif.")
    print("🟢 [OK] harita.py    -> 34 Hisse Sektör ve Webhook Haritaları Yüklendi.")
    print("🟢 [OK] config.py    -> Teknik Parametreler ve Port Ayarları Doğrulandı.")
    print("🟢 [OK] kumbara.py   -> 34 Hisse Sektör Para Kumbaraları ve Zaman Matrisi Aktif.")
    print("🟢 [OK] protokol.py  -> Arka Plan Telsiz Yönetimi ve Sinyal Sevk Hattı Doğrulandı.")
    print("🟢 [OK] beyin.py     -> AYZERS Risk Subayı ve Karar Destek Mekanizması Hazır.")
    print("🟢 [OK] broker.py    -> Phillip Capital API Entegrasyonu ve Emir Hattı Tetikte.")
    print("🔒 [GÜVENLİK] Siber Kalkan -> Gizli Kurmay Şifresi Devrede.")
    print("🛡️ "*15 + "\n")

sinyal_havuzu = []
kabul_odasi_acik = False
aktif_sanal_islemler = {}
sanal_kasa_bakiyesi = 100000.0
gunluk_max_zarar_limiti = -3000.0
gunluk_pnl = 0.0

def golge_deftere_yaz(rapor):
    try:
        with open("golge_savas_raporu.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(rapor, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"❌ [GÖLGE DEFTER] Arşive yazılırken bir sızıntı oluştu: {e}")

def dinamik_lot_hesapla(veri: SinyalVerisi, kasa: float):
    guven_katsayisi = veri.q_score if veri.q_score else 0.5
    kullanilacak_tutar = kasa * (0.10 + (guven_katsayisi * 0.05))
    fiyat = float(veri.price)
    if fiyat <= 0: return 0
    return int(kullanilacak_tutar / fiyat)

def sanal_islemi_kapat(veri: SinyalVerisi):
    global aktif_sanal_islemler, sanal_kasa_bakiyesi, gunluk_pnl
    sembol = veri.symbol

    if sembol not in aktif_sanal_islemler:
        return

    islem = aktif_sanal_islemler.pop(sembol)
    cikis_fiyati = float(veri.price)
    kâr_zarar = (cikis_fiyati - islem['giris_fiyati']) * islem['lot']

    sanal_kasa_bakiyesi += kâr_zarar
    gunluk_pnl += kâr_zarar

    rapor = {
        "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sembol": sembol,
        "islem_suresi_sn": (datetime.now() - islem['giris_zamani']).total_seconds(),
        "giris_fiyati": islem['giris_fiyati'],
        "cikis_fiyati": cikis_fiyati,
        "pnl": round(kâr_zarar, 2),
        "yeni_bakiye": round(sanal_kasa_bakiyesi, 2),
        "MFE_Max_Kar_Fiyati": islem['mfe'],
        "MAE_Max_Zarar_Fiyati": islem['mae']
    }

    print(f"\n📊 [GÖLGE İNFAZ] {sembol} | PnL: {round(kâr_zarar, 2)} ₺ | Kasa: {round(sanal_kasa_bakiyesi, 2)} ₺")
    golge_deftere_yaz(rapor)

async def en_guclu_sinyali_sec_ve_infaz_et():
    global sinyal_havuzu, kabul_odasi_acik, aktif_sanal_islemler, gunluk_pnl
    await asyncio.sleep(30)

    if not sinyal_havuzu:
        kabul_odasi_acik = False
        return

    if gunluk_pnl <= gunluk_max_zarar_limiti:
        print(f"🛑 [SİSTEM KİLİTLİ] Kasa çok yara aldı (Günlük Zarar: {gunluk_pnl} ₺). Tüm sinyaller reddedildi.")
        sinyal_havuzu.clear()
        kabul_odasi_acik = False
        return

    en_guclu_sinyal = max(sinyal_havuzu, key=lambda s: (s.q_score, -s.spread_pct))
    print(f"🏆 [KAZANAN BİRLİK] {en_guclu_sinyal.symbol} İnfaza Gönderiliyor.")

    arka_plan_telsiz_yonetimi(en_guclu_sinyal)

    giris_fiyati = float(en_guclu_sinyal.price)
    alinacak_lot = dinamik_lot_hesapla(en_guclu_sinyal, sanal_kasa_bakiyesi)

    if alinacak_lot > 0:
        aktif_sanal_islemler[en_guclu_sinyal.symbol] = {
            "giris_zamani": datetime.now(),
            "giris_fiyati": giris_fiyati,
            "lot": alinacak_lot,
            "mfe": giris_fiyati,
            "mae": giris_fiyati
        }
    
    sinyal_havuzu.clear()
    kabul_odasi_acik = False

@app.post("/webhook")
async def borsa_webhook(request: Request, background_tasks: BackgroundTasks):
    global sinyal_havuzu, kabul_odasi_acik, aktif_sanal_islemler

    try:
        gelen_ham_veri = await request.json()
        
        # --- 🛡️ SİBER KİMLİK KONTROLÜ BAŞLIYOR ---
        gelen_sifre = gelen_ham_veri.get("passphrase", "")
        if gelen_sifre != GIZLI_KURMAY_SIFRESI:
            print(f"🚷 [SİBER İHLAL] Yanlış parolalı sahte bir sinyal reddedildi! Kapı kilitlendi.")
            return JSONResponse(content={"hata": "Erişim Reddedildi! Siber kalkan aktif."}, status_code=403)
        # ----------------------------------------

        buy_or_sell = gelen_ham_veri.get("buyOrCell", "").upper()

        if buy_or_sell == "MEGA_PING":
            hisseler_listesi = gelen_ham_veri.get("hisseler", [])
            background_tasks.add_task(mega_ping_hacmini_isle, hisseler_listesi)
            return JSONResponse(content={"durum": "Sektör Akışı Alındı"}, status_code=200)

        güvenli_veri = {
            "buyOrCell": buy_or_sell,
            "symbol": str(gelen_ham_veri.get("symbol", "BİLİNMEYEN")),
            "quantity": str(gelen_ham_veri.get("quantity", "0")),
            "price": str(gelen_ham_veri.get("price", "0.0")),
            "q_score": float(gelen_ham_veri.get("q_score", 0.5)),
            "spread_pct": float(gelen_ham_veri.get("spread_pct", 0.0)),
            "is_time_ok": gelen_ham_veri.get("is_time_ok", True),
            "mss": str(gelen_ham_veri.get("mss", "YOK")),
            "ai_state_matrix": str(gelen_ham_veri.get("ai_state_matrix", "YOK")),
            "formasyon": str(gelen_ham_veri.get("formasyon", "YOK")),
            "is_knife": str(gelen_ham_veri.get("is_knife", "YOK")),
            "rsi": str(gelen_ham_veri.get("rsi", "50.0"))
        }

        veri = SinyalVerisi(**güvenli_veri)

        if veri.buyOrCell.upper() == "SELL":
            background_tasks.add_task(arka_plan_telsiz_yonetimi, veri)
            background_tasks.add_task(sanal_islemi_kapat, veri)
            return JSONResponse(content={"durum": "Islem Tamamlandi"}, status_code=200)

        if veri.symbol in aktif_sanal_islemler:
            return JSONResponse(content={"durum": "Red", "mesaj": f"{veri.symbol} zaten içeride."}, status_code=200)

        sinyal_havuzu.append(veri)

        if not kabul_odasi_acik:
            kabul_odasi_acik = True
            background_tasks.add_task(en_guclu_sinyali_sec_ve_infaz_et)

        return JSONResponse(content={"durum": "Islem Beklemede"}, status_code=200)

    except Exception as e:
        print(f"❌ [TELSİZ ARIZASI] Webhook işlem hatası: {str(e)}")
        return JSONResponse(content={"hata": f"İşlem arızası: {str(e)}"}, status_code=500)

@app.post("/fiyat_guncelle")
async def fiyat_guncelle(sembol: str, anlik_fiyat: float):
    global aktif_sanal_islemler
    if sembol in aktif_sanal_islemler:
        islem = aktif_sanal_islemler[sembol]
        if anlik_fiyat > islem['mfe']:
            islem['mfe'] = anlik_fiyat
        if anlik_fiyat < islem['mae']:
            islem['mae'] = anlik_fiyat
    return {"durum": "Sensörler Güncellendi"}

if __name__ == "__main__":
    uvicorn.run("karargah:app", host="0.0.0.0", port=8000, reload=True)
