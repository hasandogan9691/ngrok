# modeller.py
from pydantic import BaseModel
from typing import Optional, List, Union

# # [EK] TradingView'dan gelen zenginleştirilmiş 18 parametreli tam telemetri haritası
class SinyalVerisi(BaseModel):
    buyOrCell: str
    symbol: str
    quantity: str
    price: str
    mss: Union[bool, str]
    ai_state_matrix: Union[int, str]
    formasyon: str

    # Protokol Sensörleri
    is_time_ok: bool
    spread_pct: float
    is_knife: Union[bool, str]
    q_score: float
    rsi: Union[float, str]

    # Pine Script'ten Gelen Taktiksel Telemetri Paketleri
    ana_trend_boga: Optional[bool] = None
    ucuz_bolgede_mi: Optional[bool] = None
    cvd_delta: Optional[float] = None
    q_savunma_katsayisi: Optional[float] = None
    ob_doluluk_orani: Optional[float] = None
    aktif_silahlar: Optional[List[int]] = None
    hacim: Optional[float] = 0.0
# //[EK] karargah.py bünyesindeki tamir matrisinin enjekte edebileceği "YOK" string verilerine karşı Pydantic şemasını 422 doğrulama çökmelerinden koruyan Union (Hibrit Tip) zırhı eklendi.
