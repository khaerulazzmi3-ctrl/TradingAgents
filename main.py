import os

# Set environment variables sebelum mengimpor modul TradingAgents
groq_key = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_API_KEY"] = groq_key or ""

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

config = DEFAULT_CONFIG.copy()

# Atur provider dan model untuk Groq
config["llm_provider"] = "groq"
config["quick_think_llm"] = "llama-3.3-70b-versatile"
config["deep_think_llm"] = "llama-3.3-70b-versatile"
config["backend_url"] = "https://api.groq.com/openai/v1"
config["api_key"] = groq_key

# Inisialisasi TradingAgents
ta = TradingAgentsGraph(debug=True, config=config)

print("--- Menjalankan Analisis AI Agent ---")
_, decision = ta.propagate("NVDA", "2026-09-01")
print("Hasil Keputusan AI:", decision)
