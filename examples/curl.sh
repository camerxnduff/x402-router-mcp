# Search: cheapest reliable weather APIs on Base
curl -s "https://router-production-ab89.up.railway.app/dashboardapi/endpoints?q=weather&chain=Base&min_score=90&sort=price&limit=5"
# Best single match (free)
curl -s -X POST https://router-production-ab89.up.railway.app/route -H 'content-type: application/json' -d '{"category":"Finance","chain":"Base","max_price":0.05}'
# Paid route: returns 402 + payment requirements; pay with any x402 client
curl -si -X POST https://router-production-ab89.up.railway.app/route/paid -H 'content-type: application/json' -d '{"q":"weather"}'
