# protokol.py

import json
import requests
import re
# //[EK] Llama 3 modelinin ürettiği metinlerin içindeki saf JSON objesini cımbızla söküp almak için eklenen düzenli ifadeler kütüphanesi.
from config import OLLAMA_URL
from harita import PHILLIP_WEBHOOK_HARITASI
from doktrin import SYSTEM_PROMPT
from modeller import SinyalVerisi

# //[EK] Donanımsal güvenlik duvarı
def risk_suzgeci(veri: SinyalVerisi):
    if veri.buyOrCell.upper() == "SELL":
        return True, "ONAY: Satış (Çıkış) emri, güvenlik süzgeçlerinden muaf tutularak işleme alındı."

    if not veri.is_time_ok:
        return False, "RED: İşlem saatleri dışında veya mola vaktinde sinyal alındı."
    if veri.spread_pct > 0.30:
        return False, "RED: Anlık makas (spread) tolerans sınırını (%0.30) aşıyor."
    if veri.is_knife:
        return False, "RED: Düşen bıçak (c_is_knife) tespit edildi, piyasa çok volatil."
    if veri.q_score < -0.5:
        return False, "RED: AI (Q-Table) bu piyasa koşulunda (State) zarar riskini yüksek buldu."
    
    return True, "ONAY: Tüm temel donanımsal güvenlik katmanları geçildi."

# //[EK] Phillip Capital İnfaz Birimi
def phillip_capital_emir_gonder(veri: SinyalVerisi):
    webhook_url = PHILLIP_WEBHOOK_HARITASI.get(veri.symbol.upper())

    if not webhook_url:
        print(f"⚠️ [SİSTEM UYARISI] {veri.symbol} için tanımlanmış bir Phillip Capital Webhook URL'si bulunamadı!")
        return False

    emir_paketi = {
        "buyOrCell": veri.buyOrCell.upper(),
        "orderType": "LMT",
        "seance": "GUN",
        "symbol": veri.symbol,
        "quantity": veri.quantity,
        "price": veri.price,
        "eveningSeance": "0"
    }

    headers = {"Content-Type": "application/json"}

    try:
        # requests.post(webhook_url, json=emir_paketi, headers=headers)
        print(f"🚀 [EMİR İNFAZ] {veri.symbol} ({veri.buyOrCell}) {veri.quantity} Lot -> {veri.price} ₺ seviyesinden iletildi.")
        print(f"📦 [GİDEN PAKET] {json.dumps(emir_paketi)}")
        return True
    except Exception as e:
        print(f"❌ [EMİR HATASI] Broker bağlantı hatası: {str(e)}")
        return False

# //[EK] Arka Plan Llama 3 Yürütücüsü
def arka_plan_yapay_zeka_analizi(veri: SinyalVerisi):
    print("\n" + "="*60)
    print(f"🧠 [GMN MATRIX] {veri.symbol} ({veri.buyOrCell}) için Algoritmik Risk Subayı uyandırıldı...")

    durum, gerekce = risk_suzgeci(veri)
    
    if not durum:
        print(f"🛑 [BLOKE - DONANIM SÜZGECİ] {gerekce}")
        print("="*60 + "\n")
        return

    print("✅ [DONANIM SÜZGECİ GEÇİLDİ] Sinyal Llama 3 birimine sevk ediliyor...")

    if veri.buyOrCell.upper() == "SELL":
        print(f"🚨 [BYPASS] {veri.symbol} SELL emri. Llama 3 filtresi es geçildi, MUTLAK ONAY verildi.")
        karar_json = {"karar": "ONAY", "gerekce": "Satış emri mutlak koruma kapsamındadır."}
        
        print(f"🤖 [LLAMA 3 KARARI]: {karar_json.get('karar')}")
        print(f"📝 [GEREKÇE]: {karar_json.get('gerekce')}")
        phillip_capital_emir_gonder(veri)
    # //[EK] Satış (SELL) emirlerinin yapay zekanın muhakeme süresine takılmadan milisaniyeler içinde onaylanıp doğrudan borsaya fırlatılmasını sağlayan emniyet köprüsü.

    else:
        tam_prompt = f"{SYSTEM_PROMPT}\n\nGELEN SINYAL VERISI:\n{veri.model_dump_json()}"
        
        payload = {
            "model": "llama3",
            "prompt": tam_prompt,
            "stream": False,
            "format": "json"
        }

        try:
            cevap = requests.post(OLLAMA_URL, json=payload)
            cevap.raise_for_status()
            ai_yaniti = cevap.json()["response"]
            
            match = re.search(r"\{.*\}", ai_yaniti, re.DOTALL)
            if match:
                karar_json = json.loads(match.group(0))
            else:
                karar_json = {"karar": "RED", "gerekce": "JSON formatı dışı gürültülü çıktı."}
            # //[EK] Llama 3'ün bazen kibarlık yapıp ürettiği süslü metinlerin veya markdown kod bloklarının gürültüsünü eritip temizleyen regex filtresi.

            print(f"🤖 [LLAMA 3 KARARI]: {karar_json.get('karar')}")
            print(f"📝 [GEREKÇE]: {karar_json.get('gerekce')}")

            if karar_json.get("karar") == "ONAY":
                phillip_capital_emir_gonder(veri)
            else:
                print(f"🛑 [BLOKE - LLAMA 3] {veri.symbol} sinyali imha edildi.")

        except Exception as e:
            print(f"❌ [YAPAY ZEKA HATASI] Llama 3 modeline ulaşılamadı veya JSON hatası: {str(e)}")
    print("="*60 + "\n")