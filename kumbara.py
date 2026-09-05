# kumbara.py

import json
from harita import SEKTOR_HARITASI

# --- 2. CANLI SEKTÖR PARA KUMBARALARI ---
SEKTOR_KUMBARALARI = {
    "Ulaştırma-Havacılık": 0.0,
    "Enerji-Elektrik": 0.0,
    "Otomotiv-Sanayi": 0.0,
    "Holding-İnşaat": 0.0,
    "Perakende-Gıda": 0.0,
    "Ağır-Sanayi": 0.0,
    "Telekomünikasyon": 0.0,
    "Teknoloji-Savunma": 0.0
}
# //[EK] Her 5 dakikada bir güncellenen hisse fiyat ve hacim çarpanlarından (Nakit Akışı) elde edilen sektörel toplamları biriktiren canlı sayaç kumbaraları.


# --- 3. ENDPOINT İÇİNDE PAKETİ GÖĞÜSLEME VE PARÇALAMA ALANI ---
# [NOT]: Bu blok FastAPI'deki webhook dinleyici fonksiyonunuzun (FastAPI Request) içine yerleştirilir.
def mega_ping_hacmini_isle(hisseler_listesi: list):

    print("\n" + "🛰️ "*20)
    print("📡 [TELEMETRİ] Radardaki 34 Hisse İçin 5 Dakikalık Olağan Sağlık Raporu Ulaştı.")

    # Python dünyasında dilediğimiz gibi döngü kurup verileri kumbaralara işliyoruz
    for hisse in hisseler_listesi:
        sembol = hisse.get("s")
        fiyat = hisse.get("p", 0.0)
        hacim = hisse.get("v", 0.0)

        # Anlık nominal para akışı hacmi = Fiyat * Hacim
        anlik_para_akisi = fiyat * hacim

        # Hissenin ait olduğu sektörü bulup kumbarasını besliyoruz
        sektor = SEKTOR_HARITASI.get(sembol)
        if sektor in SEKTOR_KUMBARALARI:
            SEKTOR_KUMBARALARI[sektor] += anlik_para_akisi

    print("📊 [SEKTÖR ROTASYONU] Canlı Para Akışları Başarıyla Güncellendi.")
    print(f"💰 Güncel Sektör Dağılımları: {json.dumps(SEKTOR_KUMBARALARI, ensure_ascii=False, indent=2)}")
    try:
        # //[EK] Kök dizin uyuşmazlıklarını önlemek adına kayıt noktası doğrudan WSL karargah rotasına mühürlendi.
        dosya_yolu = "/mnt/c/Users/Hasan Doğan/sohbet/sektor_akisi.json"
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(SEKTOR_KUMBARALARI, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Köprü yazma sızısı: {str(e)}")

    print("🛰️ "*20 + "\n")

    return {"durum": "Sektörler Güncellendi"}
# //[EK] Gelen mega JSON trenini içerisindeki hisse listesine göre parçalayan, her bir tahtanın nakit gücünü hesaplayıp ait olduğu kumbaraya saniyeler içinde dağıtan akış yürütücüsü.
