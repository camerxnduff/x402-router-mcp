import httpx
D, R = "https://dashboard-production-4344.up.railway.app", "https://router-production-ab89.up.railway.app"
hits = httpx.get(f"{D}/api/endpoints", params={"q": "weather", "chain": "Base", "limit": 5}).json()
for e in hits["endpoints"]:
    print(e["score"], e["price_usdc"], e["url"])
best = httpx.post(f"{R}/route", json={"q": "weather", "chain": "Base"}).json()
print("route to:", best.get("target_url"), "total", best.get("total"))
# To call the paid target, use an x402 client (e.g. pip install x402) with your own wallet.
