# x402 Router: find and pay the right x402 API in one call
**20,700+ LIVE x402 endpoints across 3,100+ services, probed every 3 hours and scored 0-100 for reliability.**
Agents don't need to know which pay-per-call API is up. Ask the router.

- Dashboard: https://dashboard-production-4344.up.railway.app
- Router: https://router-production-ab89.up.railway.app  (OpenAPI: https://router-production-ab89.up.railway.app/openapi.json · x402 discovery: https://router-production-ab89.up.railway.app/.well-known/x402)
- For LLMs: https://dashboard-production-4344.up.railway.app/llms.txt

## Why
Thousands of x402 endpoints exist, and many are dead, misconfigured or slow. We probe every one, check that its 402 body is valid (version, scheme, network, payTo, asset, amount), and rank by uptime and latency.

## Free APIs (no key, no account)
| Endpoint | What |
|---|---|
| GET https://dashboard-production-4344.up.railway.app/api/endpoints?q=&chain=&category=&max_price=&min_score=&sort=&limit= | Search LIVE endpoints, best first |
| GET https://dashboard-production-4344.up.railway.app/api/summary | Counts by chain, category, source |
| GET https://dashboard-production-4344.up.railway.app/api/registry | Full registry (gzip) |
| POST https://router-production-ab89.up.railway.app/route | Best single match (free preview) |
| POST https://router-production-ab89.up.railway.app/route/paid | Same, x402-paid: $0.01 USDC on Base (Solana accepted) |

## Quickstart
See examples/ (curl, Python, TypeScript) and mcp-server/ for Claude, Cursor and any MCP client.

## Install the MCP server
```bash
git clone https://github.com/camerxnduff/x402-router-mcp
cd x402-router-mcp/mcp-server
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python test_client.py   # calls the live router, read-only
```
Then add to Claude Desktop / Cursor:
```json
{"mcpServers":{"x402-router":{"command":"/abs/path/x402-router-mcp/mcp-server/.venv/bin/python","args":["/abs/path/x402-router-mcp/mcp-server/server.py"]}}}
```
The server is read-only: it never holds keys and never pays.

## License
MIT
