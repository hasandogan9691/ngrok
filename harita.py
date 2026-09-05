# harita.py

# Gerçek broker haritası burada bilerek yeniden oluşturulmaz; yalnızca yetkili bir kaynaktan geri yüklenmelidir.
PHILLIP_WEBHOOK_HARITASI = {}


# --- 1. RADARDAKİ ORDUMUZUN SEKTÖREL HARİTASI ---
SEKTOR_HARITASI = {
    "ALTNY": "Teknoloji-Savunma", "ARCLK": "Otomotiv-Sanayi", "ASTOR": "Enerji-Elektrik",
    "AYGAZ": "Enerji-Elektrik", "BIMAS": "Perakende-Gıda", "BRISA": "Otomotiv-Sanayi",
    "CIMSA": "Ağır-Sanayi", "CWENE": "Enerji-Elektrik", "ENJSA": "Enerji-Elektrik",
    "ENKAI": "Holding-İnşaat", "EREGL": "Ağır-Sanayi", "EUPWR": "Enerji-Elektrik",
    "FROTO": "Otomotiv-Sanayi", "GESAN": "Enerji-Elektrik", "KCHOL": "Holding-İnşaat",
    "KORDS": "Otomotiv-Sanayi", "KRDMD": "Ağır-Sanayi", "MAVI": "Perakende-Gıda",
    "MGROS": "Perakende-Gıda", "OYAKC": "Ağır-Sanayi", "PETKM": "Otomotiv-Sanayi",
    "PGSUS": "Ulaştırma-Havacılık", "SAHOL": "Holding-İnşaat", "SISE": "Ağır-Sanayi",
    "TAVHL": "Ulaştırma-Havacılık", "TCELL": "Telekomünikasyon", "THYAO": "Ulaştırma-Havacılık",
    "TOASO": "Otomotiv-Sanayi", "TRALT": "Ulaştırma-Havacılık", "TTKOM": "Telekomünikasyon",
    "TUPRS": "Enerji-Elektrik", "ULKER": "Perakende-Gıda", "VESTL": "Otomotiv-Sanayi",
    "YEOTK": "Enerji-Elektrik"
}
# //[EK] Gelen ham hisse sembollerinin borsa rejimine göre hangi sektörel kümeye ait olduğunu Python hafızasında saniyeler içinde bulan statik sözlük haritası.
