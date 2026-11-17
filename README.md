# x402 Router: MCP server + free API to find and pay the right x402 endpoint

[![MCP](https://img.shields.io/badge/MCP-server-blue)](https://modelcontextprotocol.io)
[![x402](https://img.shields.io/badge/x402-discovery%20%26%20router-black)](https://x402.org)
[![Chains](https://img.shields.io/badge/chains-Base%20%7C%20Solana-0052FF)](#)
[![USDC](https://img.shields.io/badge/pay-USDC-2775CA)](#)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker build](https://github.com/camerxnduff/x402-router-mcp/actions/workflows/docker.yml/badge.svg)](https://github.com/camerxnduff/x402-router-mcp/actions/workflows/docker.yml)

**24,000+ LIVE x402 pay-per-call endpoints across 3,800+ services, probed every 3 hours and scored 0-100 for reliability.**
Agents don't need to know which x402 API is up. Ask the router.

**Keywords:** x402, MCP, MCP server, AI agents, agent payments, pay-per-call APIs, USDC, Base, Solana, x402 discovery, x402 router, x402 registry, HTTP 402.

- **Live router:** https://router-production-ab89.up.railway.app (OpenAPI: [/openapi.json](https://router-production-ab89.up.railway.app/openapi.json) · x402 discovery: [/.well-known/x402](https://router-production-ab89.up.railway.app/.well-known/x402) · health: [/health](https://router-production-ab89.up.railway.app/health))
- **Dashboard / registry:** https://router-production-ab89.up.railway.app/dashboard
- **Status (uptime, crawl freshness, on-chain receipts):** https://router-production-ab89.up.railway.app/status
- **For LLMs:** https://router-production-ab89.up.railway.app/llms.txt

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
curl -s 'https://router-production-ab89.up.railway.app/api/endpoints?q=weather&chain=Base&limit=5'
```

## Why
Thousands of x402 endpoints exist, and many are dead, misconfigured or slow. The router probes every one, checks that its 402 body is valid (version, scheme, network, payTo, asset, amount), and ranks by uptime and latency, so an agent gets a working endpoint with a known price.

## HTTP API
| Endpoint | What |
|---|---|
| `GET /api/endpoints?q=&chain=&category=&max_price=&min_score=&sort=&limit=` | Search LIVE endpoints, best first |
| `GET /api/summary` | Counts by chain, category, source |
| `GET /api/registry` | Full registry (gzip) |
| `POST /route` (router) | Best match + top 3, free |
| `POST /route/paid` (router) | **$0.01 USDC** (x402, Base; Solana accepted): full ranked list (up to 25) with latency, reliability, price, payTo/networks and a ready-to-pay best pick |
| `GET /check/paid?url=` (router) | **$0.002 USDC** (x402): fresh live probe of one endpoint: is it up, latency, the real price and payTo it asks for now |

Examples: [`examples/`](examples) (curl, Python, TypeScript) and [`examples/frameworks/`](examples/frameworks) (LangChain, CrewAI, Coinbase AgentKit, x402 clients). Guides: https://router-production-ab89.up.railway.app/integrations

## MCP tools
| Tool | Cost |
|---|---|
| `search_x402_endpoints`, `route_x402_request`, `get_registry_stats`, `get_paid_route_requirements` | Free |
| `find_best_x402_endpoint` | $0.01 USDC per call |
| `check_x402_endpoint` | $0.002 USDC per call |

Paid tools pay inside the tool call. To enable them:
```bash
pip install "x402-router-mcp[pay] @ git+https://github.com/camerxnduff/x402-router-mcp#subdirectory=mcp-server"
export X402_EVM_PRIVATE_KEY=0x...      # a dedicated, low-balance Base wallet holding a little USDC
export X402_MAX_PAYMENT_USD=0.01       # per-call cap (default 0.01)
```
Without a key, the paid tools return the price and the x402 payment requirements instead of paying.

## Trust and transparency
- **Public status page:** [/status](https://router-production-ab89.up.railway.app/status) ([JSON](https://router-production-ab89.up.railway.app/status.json)) shows uptime, the last successful crawl, LIVE counts and every settled payment with a block-explorer link. Numbers come from the router's own counters and settle log; nothing is estimated.
- **Machine-readable discovery:** [/.well-known/x402](https://router-production-ab89.up.railway.app/.well-known/x402), [/.well-known/ard.json](https://router-production-ab89.up.railway.app/.well-known/ard.json), [/.well-known/agent-card.json](https://router-production-ab89.up.railway.app/.well-known/agent-card.json), [/openapi.json](https://router-production-ab89.up.railway.app/openapi.json), [/llms.txt](https://router-production-ab89.up.railway.app/llms.txt).
- **This MCP server is read-only by default:** no keys, no payments. The optional paid tools only pay when you set your own wallet key, and each call is capped by `X402_MAX_PAYMENT_USD`.

## Payments
x402 v2: Base USDC first, Solana USDC as fallback, settled through the PayAI facilitator.

## License
MIT
