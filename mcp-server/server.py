"""x402 Router MCP server: search ~21k LIVE x402 endpoints and pick the best one.
Read-only; calls public APIs; holds no keys and never pays.
Run: python server.py            (stdio)
     python server.py --http 8000 (streamable HTTP at /mcp)"""
import os, sys, httpx
from mcp.server.fastmcp import FastMCP

ROUTER = os.environ.get("X402_ROUTER_URL", "https://router-production-ab89.up.railway.app")
DASH = os.environ.get("X402_DASHBOARD_URL", "https://dashboard-production-4344.up.railway.app")
mcp = FastMCP("x402-router")
_c = httpx.Client(timeout=30, headers={"user-agent": "x402-router-mcp/0.1"})

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
    """Ask the x402 Router for the single best-scored LIVE endpoint matching filters (free POST /route).
    Returns target URL, method, price, 1% router fee and total. Does not pay or call the target."""
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

if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.settings.port = int(sys.argv[sys.argv.index("--http")+1]) if len(sys.argv) > sys.argv.index("--http")+1 else 8000
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
