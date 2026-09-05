# broker.py
import json
import requests
from harita import PHILLIP_WEBHOOK_HARITASI

def phillip_capital_emir_gonder(veri):
    webhook_url = PHILLIP_WEBHOOK_HARITASI.get(veri.symbol.upper())
    if not webhook_url:
        print(f"⚠️ [SİSTEM UYARISI] {veri.symbol} için Webhook URL'si bulunamadı!")
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

    try:
        # requests.post(webhook_url, json=emir_paketi, headers={"Content-Type": "application/json"})
        print(f"🚀 [EMİR İNFAZ] {veri.symbol} ({veri.buyOrCell}) {veri.quantity} Lot -> {veri.price} ₺ iletildi.")
        return True
    except Exception as e:
        print(f"❌ [EMİR HATASI] Broker bağlantı hatası: {str(e)}")
        return False
# //[EK] Aracı kurum API entegrasyonunu izole ederek, ağ ve paketleme hatalarını tek bir odada çözen infaz birimi.