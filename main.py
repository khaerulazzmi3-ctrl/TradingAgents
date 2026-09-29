from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "groq"
config["quick_think_llm"] = "llama-3.3-70b-versatile"
config["deep_think_llm"] = "llama-3.3-70b-versatile"

ta = TradingAgentsGraph(debug=True, config=config)

print("--- Menjalankan Analisis AI Agent ---")
_, decision = ta.propagate("NVDA", "2026-09-01")
print("Hasil Keputusan AI:", decision)
