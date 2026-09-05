import csv
import json
import re

# AYZERS'in ruhunu (91 Maddelik Doktrin) içeri aktarıyoruz.
from doktrin import SISTEM_KURALLARI

CSV_DOSYASI = "hasat.csv"
JSONL_DOSYASI = "egitim_verisi.jsonl"
SEMBOL = "TTKOM" 

print("⏳ AYZERS Zırhlı Veri Fabrikası çalıştırılıyor. Hammadde taranıyor...")

try:
    with open(CSV_DOSYASI, mode='r', encoding='utf-8-sig') as f:
        ayrac = ';' if ';' in f.readline() else ','

    with open(CSV_DOSYASI, mode='r', encoding='utf-8-sig') as csv_file, open(JSONL_DOSYASI, mode='a', encoding='utf-8') as jsonl_file:
        reader = csv.DictReader(csv_file, delimiter=ayrac)
        headers = reader.fieldnames

        fiyat_sutunu = next((col for col in headers if col and ("Price" in col or "Fiyat" in col)), None)
        sinyal_sutunu = next((col for col in headers if col and ("Signal" in col or "Sinyal" in col)), None)
        tip_sutunu = next((col for col in headers if col and ("Tip" in col or "Type" in col)), None)

        uretilen_veri_sayisi = 0

        for row in reader:
            sinyal_metni = str(row.get(sinyal_sutunu, ""))
            tip_metni = str(row.get(tip_sutunu, ""))
            
            # //[EK] Zırhlı Sinyal Radarı: Giriş işlemi olduğunu gösteren herhangi bir kelimeyi yakalar.
            if "SMC_AL" in sinyal_metni or "BOS+OB" in sinyal_metni or "Giriş" in tip_metni or "Entry" in tip_metni:
                
                ham_fiyat = str(row[fiyat_sutunu])
                
                # //[EK] Cerrahi Rakam Temizleyici (Regex): Harfleri, "TRY" yazılarını ve boşlukları siler.
                temiz_fiyat = re.sub(r'[^\d.,]', '', ham_fiyat)
                
                # //[EK] Türk (1.300,50) ve Amerikan (1,300.50) formatlarını çözen akıllı dönüştürücü.
                if '.' in temiz_fiyat and ',' in temiz_fiyat:
                    if temiz_fiyat.rfind('.') > temiz_fiyat.rfind(','):
                        temiz_fiyat = temiz_fiyat.replace(',', '')
                    else:
                        temiz_fiyat = temiz_fiyat.replace('.', '').replace(',', '.')
                elif ',' in temiz_fiyat:
                    temiz_fiyat = temiz_fiyat.replace(',', '.')

                try:
                    giris_fiyati = float(temiz_fiyat)
                except ValueError:
                    continue # Çok bozuk bir satırsa sessizce atla
                
                stop_fiyati = round(giris_fiyati * 0.99, 2)
                hisse_basi_risk = round(giris_fiyati - stop_fiyati, 2)
                
                if hisse_basi_risk <= 0: continue
                
                alinacak_lot = int(350 / hisse_basi_risk)

                # --- 🥇 ALTIN ŞABLON (KULLANICI SORUSU) ---
                user_content = f"Kaptan, {SEMBOL} grafiğinde BOS gerçekleşti. Fiyat şu an {giris_fiyati} TL ile Discount bölgesindeki güçlü bir Order Block alanına temas etti. Teknik stop seviyemiz {stop_fiyati} TL. Mevcut durumu analiz et."

                # --- 🥇 ALTIN ŞABLON (AYZERS'İN KUSURSUZ CEVABI) ---
                assistant_content = f"""KAPTAN, ANALİZ:

1. Genel Görünüm
Mevcut piyasa durumunda fiyatın iskontolu (Discount) bölgeye çekilmesiyle alım yönlü (Bullish) potansiyel bir fırsat alanı oluşmuştur.

2. Trend Analizi
Ana yön yukarıdır. Önceki tepenin kırılması, alıcı gücünün devam ettiğine işaret etmektedir. Zayıflık belirtisi şu an için yoktur.

3. Teknik Seviyeler
- Destek (Geçersizlik Noktası): {stop_fiyati} TL
- Direnç (Hedef Bölge): {round(giris_fiyati * 1.02, 2)} TL ve üzeri

4. Yapı Analizi
BOS gerçekleşmiş ve yükselen yapı teyit edilmiştir. Fiyatın mevcut durumda {giris_fiyati} TL'deki Bullish Order Block bölgesine inmesi, likidite alımı sonrası sağlıklı bir düzeltme hareketidir.

5. Senaryolar
- Pozitif Senaryo: Fiyatın {giris_fiyati} TL'deki Order Block bölgesinden tepki alması ve 3 mumluk hacimli teyit oluşturması beklenir.
- Negatif Senaryo: Fiyatın {stop_fiyati} TL desteği altında hacimli mum kapanışı yapması (CHOCH tehlikesi).

6. Riskler ve Pozisyon Yönetimi
Piyasada anlık volatilite risklerine karşı sermaye koruma protokolü devrededir. Doktrin kurallarına göre hesaplanan pozisyon boyutu şu şekildedir:
- Sermaye: 10.000 TL
- İşlem Riski (Maksimum): 350 TL
- Giriş Fiyatı: {giris_fiyati} TL
- Stop Mesafesi: {stop_fiyati} TL
- Hisse Başına Risk: {hisse_basi_risk} TL
- Pozisyon Büyüklüğü: 350 / {hisse_basi_risk} = {alinacak_lot} Adet {SEMBOL}

7. Sonuç
Sistem kurallarına uygun, risk/ödül oranı makul ve disiplinli bir SMC işlem kurulumu mevcuttur. Sermaye güvenliği için {alinacak_lot} adetlik pozisyon sınırı kesinlikle aşılmamalıdır."""

                json_satiri = {
                    "messages": [
                        {"role": "system", "content": SISTEM_KURALLARI},
                        {"role": "user", "content": user_content},
                        {"role": "assistant", "content": assistant_content}
                    ]
                }

                jsonl_file.write(json.dumps(json_satiri, ensure_ascii=False) + '\n')
                uretilen_veri_sayisi += 1

    if uretilen_veri_sayisi > 0:
        print(f"✅ Üretim Tamamlandı! {uretilen_veri_sayisi} adet kusursuz SMC senaryosu 'egitim_verisi.jsonl' dosyasına başarıyla basıldı.")
    else:
        print("⚠️ Uyarı: Okunacak satır kalmadı veya CSV'de 'Giriş' işlemi bulunamadı.")

except Exception as e:
    print(f"Üretim bandında beklenmeyen bir hata oluştu: {e}")
