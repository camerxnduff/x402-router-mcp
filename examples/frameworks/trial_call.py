# pip install httpx
# Free trial of X402 Router's /route/paid: 3 free calls per wallet and per IP per UTC day, no payment needed.
# Falls back to telling you the price when the trial is used up (then use paid_client.py).
import os, httpx

ROUTER = os.environ.get("X402_ROUTER_URL", "https://router-production-ab89.up.railway.app")
WALLET = os.environ["WALLET"]   # your EVM 0x... or Solana address (only used as the trial key; nothing is signed)

def route_trial(q, chain=None, max_price=None, category=None):
    body = {k: v for k, v in {"q": q, "chain": chain, "max_price": max_price, "category": category}.items() if v is not None}
    r = httpx.post(ROUTER + "/route/paid", json=body, headers={"X-402-Trial": WALLET}, timeout=30)
    left = r.headers.get("X-402-Trial-Remaining")
    if r.status_code == 402:
        return {"trial_used_up": True, "remaining": left, "next": "pay 0.01 USDC per call with an x402 client (paid_client.py)"}
    r.raise_for_status()
    return {"remaining": left, **r.json()}

if __name__ == "__main__":
    out = route_trial("weather", chain="Base")
    print("trial calls left today:", out.get("remaining"))
    print(out.get("best", out))
