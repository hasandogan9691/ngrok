# protokol.py
from beyin import yapay_zeka_onay_istegi
from broker import phillip_capital_emir_gonder
from kumbara import mega_ping_hacmini_isle

def risk_suzgeci(veri):
    if veri.buyOrCell.upper() == "SELL":
        return True, "ONAY: Satış emri, süzgeçlerden muaf."
    if not veri.is_time_ok:
        return False, "RED: İşlem saatleri dışında sinyal."
    if veri.spread_pct > 0.30:
        return False, "RED: Makas toleransı aşıldı."
    return True, "ONAY: Donanım geçildi."

def arka_plan_telsiz_yonetimi(veri):
    print("\n" + "="*60)

    # --- MEGA_PING GELDİYSE DOĞRUDAN KUMBARAYA SEVK ET ---
    if getattr(veri, "buyOrCell", "").upper() == "MEGA_PING":
        mega_ping_hacmini_isle(getattr(veri, "hisseler", []))
        print("="*60 + "\n")
        return {
            "karar": "MEGA_PING",
            "gerekce": "MEGA_PING hacim verisi kumbaraya sevk edildi.",
            "broker_gonderildi": False,
        }

    # --- NORMAL ALIM SATIM SİNYALİ GELDİYSE PROTOKOLÜ İŞLET ---
    durum, gerekce = risk_suzgeci(veri)
    if not durum:
        print(f"🛑 [BLOKE] {gerekce}\n" + "="*60 + "\n")
        return {
            "karar": "RED",
            "gerekce": gerekce,
            "broker_gonderildi": False,
        }

    # Satiş ise AYZERS'e sormadan doğrudan infaza gönder
    if veri.buyOrCell.upper() == "SELL":
        print(f"🚨 [BYPASS] {veri.symbol} SELL emri mutlak onaylandı.")
        broker_gonderildi = bool(phillip_capital_emir_gonder(veri))
        sonuc = {
            "karar": "ONAY",
            "gerekce": gerekce,
            "broker_gonderildi": broker_gonderildi,
        }
    else:
        # Alım ise Beyin dosyasına sor
        onay_durumu = yapay_zeka_onay_istegi(veri.model_dump_json())
        if onay_durumu.get("karar") == "ONAY":
            broker_gonderildi = bool(phillip_capital_emir_gonder(veri))
            sonuc = {
                "karar": "ONAY",
                "gerekce": onay_durumu.get("gerekce", "AI onayı alındı."),
                "broker_gonderildi": broker_gonderildi,
            }
        else:
            ai_gerekcesi = onay_durumu.get("gerekce", "AI onayı alınamadı.")
            print(f"🛑 [BLOKE - AI] {veri.symbol} sinyali reddedildi: {ai_gerekcesi}")
            sonuc = {
                "karar": "RED",
                "gerekce": ai_gerekcesi,
                "broker_gonderildi": False,
            }

    print("="*60 + "\n")
    return sonuc
# //[EK] Gelen telsiz çağrısının türünü okuyarak onu doğru birimlere (AYZERS Karargahı, kumbara veya aracı kurum) şefkatle ve hızla yönlendiren komuta kontrol merkezi. Karargah onaylı.
