import json
import os
# import requests
# //[EK] Ollama'nın eski requests kütüphanesi yerine OpenAI telsiz kütüphanesi eklendi.
from openai import OpenAI

# Ollama'nın Karargah içindeki yerel iletişim adresi
# OLLAMA_API_URL = "http://localhost:11434/api/chat"
# //[EK] AYZERS'in Karargah içindeki yerel LM Studio iletişim adresi tanımlandı.
LM_STUDIO_API_URL = "http://192.168.1.45:1234/v1"
client = OpenAI(base_url=LM_STUDIO_API_URL, api_key="lm-studio")

DOKTRIN_DOSYASI = "subay_doktrin.txt"

def doktrin_oku():
    """Subayın kurallarını harici txt dosyasından okur."""
    try:
        with open(DOKTRIN_DOSYASI, "r", encoding="utf-8") as dosya:
            return dosya.read()
    except FileNotFoundError:
        print(f"KRİTİK HATA: {DOKTRIN_DOSYASI} bulunamadı! Subay kuralsız başlatılamaz.")
        exit()

def subayla_konus():
    print("="*60)
    print("🛡️ ÖZEL YAPAY ZEKA RİSK SUBAYI DEVREDE 🛡️")
    print(f"Kurallar '{DOKTRIN_DOSYASI}' dosyasından yüklendi.")
    print("Çıkmak ve subayı uyutmak için 'kapat' yazın.")
    print("="*60)

    # Kuralları dosyadan çek ve hafızaya yerleştir
    system_prompt = doktrin_oku()
    mesaj_gecmisi = [
        {"role": "system", "content": system_prompt}
    ]

    while True:
        kullanici_girdisi = input("\nMareşal: ")

        if kullanici_girdisi.lower() == 'kapat':
            print("\nSubay: Emredersiniz Komutanım. Nöbeti devrediyorum, yollarınız açık olsun.")
            break

        if not kullanici_girdisi.strip():
            continue

        mesaj_gecmisi.append({"role": "user", "content": kullanici_girdisi})

        try:
            print("Subay Düşünüyor...", end="\r")
            
            # //[EK] Ollama payload'ı iptal edildi, LM Studio (OpenAI) sohbet tamamlama isteği ateşlendi.
            response = client.chat.completions.create(
                model="ayzers",
                messages=mesaj_gecmisi,
                temperature=0.1
            )

            subay_cevabi = response.choices[0].message.content
            print(" "*20, end="\r") # Düşünüyor yazısını temizle
            print(f"Risk Subayı: {subay_cevabi}")

            # Subayın cevabını da hafızaya ekle ki sohbetin akışını unutmasın
            mesaj_gecmisi.append({"role": "assistant", "content": subay_cevabi})

        except Exception as e:
            # //[EK] Hata mesajı LM Studio motoruna göre güncellendi.
            print(f"\nBağlantı Hatası: Karargah motoru (LM Studio) yanıt vermiyor. Lütfen motorun şalterinin açık olduğunu teyit edin. Detay: {e}")

if __name__ == "__main__":
    subayla_konus()
# //[EK] Terminal tabanlı saf iletişim modülü AYZERS frekansına başarıyla senkronize edildi.
