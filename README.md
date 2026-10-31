# x402 Router: MCP server + free API to find and pay the right x402 endpoint

[![MCP](https://img.shields.io/badge/MCP-server-blue)](https://modelcontextprotocol.io)
[![x402](https://img.shields.io/badge/x402-discovery%20%26%20router-black)](https://x402.org)
[![Chains](https://img.shields.io/badge/chains-Base%20%7C%20Solana-0052FF)](#)
[![USDC](https://img.shields.io/badge/pay-USDC-2775CA)](#)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker build](https://github.com/camerxnduff/x402-router-mcp/actions/workflows/docker.yml/badge.svg)](https://github.com/camerxnduff/x402-router-mcp/actions/workflows/docker.yml)

**20,700+ LIVE x402 pay-per-call endpoints across 3,100+ services, probed every 3 hours and scored 0-100 for reliability.**
Agents don't need to know which x402 API is up. Ask the router.

**Keywords:** x402, MCP, MCP server, AI agents, agent payments, pay-per-call APIs, USDC, Base, Solana, x402 discovery, x402 router, x402 registry, HTTP 402.

- **Live router:** https://router-production-ab89.up.railway.app (OpenAPI: [/openapi.json](https://router-production-ab89.up.railway.app/openapi.json) · x402 discovery: [/.well-known/x402](https://router-production-ab89.up.railway.app/.well-known/x402) · health: [/health](https://router-production-ab89.up.railway.app/health))
- **Dashboard / registry:** https://router-production-ab89.up.railway.app/dashboard
- **For LLMs:** https://router-production-ab89.up.railway.app/dashboardllms.txt

## Quick start (MCP, 30 seconds)

The server is **read-only**: it holds no keys and never pays. It exposes four tools:
`search_x402_endpoints`, `route_x402_request`, `get_registry_stats`, `get_paid_route_requirements`.

### Option A: uvx (no clone, no PyPI needed)
Claude Desktop (`claude_desktop_config.json`) or Cursor (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "x402-router": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/camerxnduff/x402-router-mcp#subdirectory=mcp-server", "x402-router-mcp"]
    }
  }
}
```

### Option B: Docker
```json
{
  "mcpServers": {
    "x402-router": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "ghcr.io/camerxnduff/x402-router-mcp:latest"]
    }
  }
}
```
Or build it yourself: `docker build -t x402-router-mcp .` and use `x402-router-mcp` as the image name.

### Option C: from source
```bash
git clone https://github.com/camerxnduff/x402-router-mcp
cd x402-router-mcp/mcp-server
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python test_client.py   # calls the live router, read-only
```
```json
{"mcpServers":{"x402-router":{"command":"/abs/path/x402-router-mcp/mcp-server/.venv/bin/python","args":["/abs/path/x402-router-mcp/mcp-server/server.py"]}}}
```
Streamable HTTP: `python server.py --http 8000` serves `http://localhost:8000/mcp`.
Env overrides: `X402_ROUTER_URL`, `X402_DASHBOARD_URL`.

## Try it with no install (curl)
```bash
# best live Base endpoint for a category (free preview)
curl -s -X POST https://router-production-ab89.up.railway.app/route \
  -H 'content-type: application/json' -d '{"category":"Finance","chain":"Base"}'

# search the registry
curl -s 'https://router-production-ab89.up.railway.app/dashboardapi/endpoints?q=weather&chain=Base&limit=5'
```

## Why
Thousands of x402 endpoints exist, and many are dead, misconfigured or slow. The router probes every one, checks that its 402 body is valid (version, scheme, network, payTo, asset, amount), and ranks by uptime and latency, so an agent gets a working endpoint with a known price.

## HTTP API
| Endpoint | What |
|---|---|
| `GET /api/endpoints?q=&chain=&category=&max_price=&min_score=&sort=&limit=` (dashboard) | Search LIVE endpoints, best first |
| `GET /api/summary` (dashboard) | Counts by chain, category, source |
| `GET /api/registry` (dashboard) | Full registry (gzip) |
| `POST /route` (router) | Best single match, free preview |
| `POST /route/paid` (router) | Same result, x402-paid: **$0.01 USDC** on Base (Solana accepted) |

Examples: [`examples/`](examples) (curl, Python, TypeScript).

## Payments
`/route/paid` speaks x402 v2: Base USDC first, Solana USDC as fallback, settled through the PayAI facilitator. The router adds a 1% routing fee on routed calls. The MCP server itself never pays; your agent's x402 client does.

## License
MIT
