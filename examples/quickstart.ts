const D = "https://dashboard-production-4344.up.railway.app", R = "https://router-production-ab89.up.railway.app";
const hits = await (await fetch(`${D}/api/endpoints?q=weather&chain=Base&limit=5`)).json();
for (const e of hits.endpoints) console.log(e.score, e.price_usdc, e.url);
const best = await (await fetch(`${R}/route`, { method: "POST", headers: { "content-type": "application/json" },
  body: JSON.stringify({ q: "weather", chain: "Base" }) })).json();
console.log("route to:", best.target_url, "total", best.total);
// Pay targets with x402-fetch: wrapFetchWithPayment(fetch, yourWalletClient)
