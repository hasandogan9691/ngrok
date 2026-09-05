# beyin.py
import re
import json
import requests
from config import OLLAMA_URL
from doktrin import SYSTEM_PROMPT

def llama_cıktısını_temizle(ham_metin: str):
    try:
        match = re.search(r"\{.*\}", ham_metin, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        print(f"❌ [JSON AYIKLAMA HATASI] Çıktı parse edilemedi: {e}")
    return None

def yapay_zeka_onay_istegi(veri_json):
    tam_prompt = f"{SYSTEM_PROMPT}\n\nGELEN SINYAL VERISI:\n{veri_json}"
    payload = {"model": "llama3", "prompt": tam_prompt, "stream": False, "format": "json"}
    
    try:
        cevap = requests.post(OLLAMA_URL, json=payload)
        cevap.raise_for_status()
        ai_yaniti = cevap.json()["response"]
        
        karar = llama_cıktısını_temizle(ai_yaniti)
        return karar if karar else {"karar": "RED", "gerekce": "Temiz JSON alınamadı."}
    except Exception as e:
        return {"karar": "RED", "gerekce": f"Model bağlantı hatası: {str(e)}"}
# //[EK] Yerel yapay zeka modelinin (Llama 3) tüm sorgu ve regex temizlik süreçlerini diğer birimlerden tamamen ayıran akıl odası.