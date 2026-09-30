import os
import requests

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph


# 1. TIMPA VARIABEL LINGKUNGAN UNTUK MEMAKSA GROQ
groq_key = os.getenv("GROQ_API_KEY")
groq_url = "https://api.groq.com/openai/v1"

os.environ["OPENAI_API_KEY"] = groq_key or ""
os.environ["OPENAI_BASE_URL"] = groq_url
os.environ["OPENAI_API_BASE"] = groq_url

# 2. FUNGSI TELEGRAM
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str) -> None:
    """Mengirim sinyal trading ke bot Telegram."""
    if not telegram_token or not telegram_chat_id:
        print("⚠️ Secret Telegram belum diset di GitHub. Pesan tidak terkirim.")
        return

    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code == 200:
            print("✅ Sinyal analisis berhasil terkirim ke Telegram!")
        else:
            print(f"❌ Telegram Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"❌ Gagal koneksi ke Telegram: {e}")


# 3. KONFIGURASI TRADING AGENT
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "groq"
config["quick_think_llm"] = "llama-3.3-70b-versatile"
config["deep_think_llm"] = "llama-3.3-70b-versatile"
config["backend_url"] = groq_url
config["api_key"] = groq_key

# 4. JALANKAN ANALISIS
ta = TradingAgentsGraph(debug=True, config=config)

symbol = "NVDA"
print(f"--- Menjalankan AI Agent untuk {symbol} ---")
_, decision = ta.propagate(symbol, "2026-09-01")

print("Hasil Keputusan AI:", decision)

# 5. FORMAT DAN KIRIM PESAN
pesan = (
    f"🤖 *AI TRADING AGENT SIGNAL*\n\n"
    f"📈 *Asset:* `{symbol}`\n"
    f"🎯 *Decision:* `{decision}`\n\n"
    f"--- Diproses via Groq Llama 3.3 ---"
)

send_telegram_message(pesan)
