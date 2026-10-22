# x402 Router MCP server
Tools: search_x402_endpoints, route_x402_request, get_registry_stats, get_paid_route_requirements.
Read-only, no keys, never pays. Install: `pip install -r requirements.txt`
- stdio: `python server.py`
- HTTP: `python server.py --http 8000` → http://localhost:8000/mcp
Claude Desktop / Cursor config:
```json
{"mcpServers":{"x402-router":{"command":"python","args":["/path/to/server.py"]}}}
```
Env overrides: X402_ROUTER_URL, X402_DASHBOARD_URL. Test: `python test_client.py` (see test_results.txt).
