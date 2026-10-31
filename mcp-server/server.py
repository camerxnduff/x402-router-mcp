"""x402 Router MCP server: search 20k+ live-tested x402 endpoints and pick the best one.
Free tools need no keys. Paid tools (find_best_x402_endpoint $0.01, check_x402_endpoint $0.002) pay the router
in USDC on Base via x402 only if you set X402_EVM_PRIVATE_KEY (a dedicated, low-balance wallet) and
`pip install "x402-router-mcp[pay]"`. Spend per call is capped by X402_MAX_PAYMENT_USD (default 0.01).
Run: python server.py            (stdio)
     python server.py --http 8000 (streamable HTTP at /mcp)"""
import os, sys, httpx
from mcp.server.fastmcp import FastMCP

ROUTER = os.environ.get("X402_ROUTER_URL", "https://router-production-ab89.up.railway.app")
DASH = os.environ.get("X402_DASHBOARD_URL", ROUTER)  # dashboard API is served by the router since Oct 2026
mcp = FastMCP("x402-router")
_c = httpx.Client(timeout=30, headers={"user-agent": "x402-router-mcp/0.2"})

def _slim(e):
    k = ("name","url","method","category","price_usdc","chains","score","latency_ms","pay_to","last_checked")
    return {x: e.get(x) for x in k}

@mcp.tool()
def search_x402_endpoints(q: str = "", chain: str = "", category: str = "", max_price: float | None = None,
                          min_score: int | None = None, sort: str = "score", limit: int = 10) -> dict:
    """Search LIVE x402 (HTTP 402 pay-per-call) endpoints. Filters: q (text), chain (Base, Solana...),
    category, max_price (USDC), min_score (0-100), sort (score|price|latency|newest), limit (1-50)."""
    p = {"q": q, "chain": chain, "category": category, "sort": sort, "limit": max(1, min(limit, 50))}
    if max_price is not None: p["max_price"] = max_price
    if min_score is not None: p["min_score"] = min_score
    r = _c.get(f"{DASH}/api/endpoints", params={k: v for k, v in p.items() if v not in ("", None)})
    r.raise_for_status(); d = r.json()
    return {"total_matches": d.get("total_matches"), "endpoints": [_slim(e) for e in d.get("endpoints", [])]}

@mcp.tool()
def route_x402_request(category: str = "", chain: str = "", max_price: float | None = None, q: str = "", agent: str = "") -> dict:
    """FREE. Best live x402 endpoint for a task plus the top 3 (POST /route). Filters: q, category, chain, max_price.
    For the full ranked list with latency/reliability and a ready-to-pay pick use find_best_x402_endpoint. Does not pay."""
    body = {k: v for k, v in {"category": category, "chain": chain, "max_price": max_price, "q": q, "agent": agent or "mcp"}.items() if v not in ("", None)}
    r = _c.post(f"{ROUTER}/route", json=body); r.raise_for_status(); return r.json()

@mcp.tool()
def get_registry_stats() -> dict:
    """Registry summary: total/LIVE counts, LIVE by chain, median price, last crawl time, router health."""
    s = _c.get(f"{DASH}/api/summary").json(); h = _c.get(f"{ROUTER}/health").json()
    return {"updated": s.get("updated"), "counts": s.get("counts"), "median_live_price": s.get("median_live_price"),
            "live_by_chain": s.get("live_by_chain"), "router": {k: h.get(k) for k in ("status","version","fee_pct","paid_route_price_usd")}}

@mcp.tool()
def get_paid_route_requirements() -> dict:
    """Return the x402 payment requirements of the paid route (/route/paid) without paying."""
    r = _c.post(f"{ROUTER}/route/paid", json={})
    return {"http_status": r.status_code, "body": r.json() if "json" in r.headers.get("content-type","") else r.text[:2000]}

MAX_PAY_USD = float(os.environ.get("X402_MAX_PAYMENT_USD", "0.01"))

def _paid_get(path: str, params: dict) -> dict:
    """GET a paid router path. Pays via x402 (Base USDC) when X402_EVM_PRIVATE_KEY is set, else returns the price/how-to."""
    url = f"{ROUTER}{path}"
    params = {k: v for k, v in params.items() if v not in ("", None)}
    key = os.environ.get("X402_EVM_PRIVATE_KEY")
    if not key:
        r = _c.get(url, params=params)
        body = r.json() if "json" in r.headers.get("content-type", "") else {}
        price = [a.get("amount") for a in body.get("accepts", [])][:1]
        return {"paid": False, "http_status": r.status_code,
                "price_usdc": int(price[0]) / 1e6 if price and str(price[0]).isdigit() else None,
                "how_to_enable": "Set X402_EVM_PRIVATE_KEY to a dedicated low-balance Base wallet holding USDC and install x402-router-mcp[pay]. "
                                 "Free alternative: route_x402_request / search_x402_endpoints.",
                "payment_required": body}
    import asyncio
    from eth_account import Account
    from x402 import x402Client
    from x402.http.clients import x402HttpxClient
    from x402.mechanisms.evm.exact.register import register_exact_evm_client
    from x402.mechanisms.evm.signers import EthAccountSigner

    async def go():
        pre = _c.get(url, params=params)
        if pre.status_code == 402:
            amts = [int(a.get("amount") or 0) for a in pre.json().get("accepts", []) if str(a.get("network", "")).startswith("eip155:8453")]
            if not amts or min(amts) / 1e6 > MAX_PAY_USD:
                return {"paid": False, "error": f"price above X402_MAX_PAYMENT_USD={MAX_PAY_USD}", "amounts": amts}
        elif pre.status_code != 200:
            return {"paid": False, "http_status": pre.status_code, "body": pre.text[:1000]}
        client = x402Client()
        register_exact_evm_client(client, EthAccountSigner(Account.from_key(key)), networks="eip155:8453")
        async with x402HttpxClient(client, timeout=60) as hc:
            r = await hc.get(url, params=params)
            out = {"paid": r.status_code == 200, "http_status": r.status_code,
                   "payment_response": r.headers.get("payment-response")}
            try: out["result"] = r.json()
            except Exception: out["result"] = r.text[:2000]
            return out
    return asyncio.run(go())

@mcp.tool()
def find_best_x402_endpoint(q: str = "", category: str = "", chain: str = "", max_price: float | None = None, agent: str = "") -> dict:
    """PAID ($0.01 USDC on Base via x402). Full ranked list (up to 25) of live-tested x402 APIs for a task, with latency,
    reliability, price, payTo/networks, plus a ready-to-pay best pick. Needs X402_EVM_PRIVATE_KEY; otherwise returns the price."""
    return _paid_get("/route/paid", {"q": q, "category": category, "chain": chain, "max_price": max_price, "agent": agent or "mcp"})

@mcp.tool()
def check_x402_endpoint(url: str, agent: str = "") -> dict:
    """PAID ($0.002 USDC on Base via x402). Fresh live probe of one registry endpoint: is it up (HTTP 402), latency,
    the real price and payTo it asks for now, and whether that matches the registry. Needs X402_EVM_PRIVATE_KEY."""
    return _paid_get("/check/paid", {"url": url, "agent": agent or "mcp"})

def main():
    if "--http" in sys.argv:
        i = sys.argv.index("--http")
        mcp.settings.host = os.environ.get("HOST", "127.0.0.1")
        mcp.settings.port = int(sys.argv[i + 1]) if len(sys.argv) > i + 1 else 8000
        mcp.run(transport="streamable-http")
    else:
        mcp.run()

if __name__ == "__main__":
    main()
