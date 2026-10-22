import asyncio, json, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
    async with stdio_client(StdioServerParameters(command=sys.executable, args=["server.py"])) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            print("TOOLS:", [t.name for t in (await s.list_tools()).tools])
            for n, a in [("get_registry_stats", {}), ("search_x402_endpoints", {"q": "weather", "chain": "Base", "limit": 3}),
                         ("route_x402_request", {"category": "Finance", "chain": "Base"}), ("get_paid_route_requirements", {})]:
                res = await s.call_tool(n, a); t = res.content[0].text
                print(f"\n== {n} error={res.isError}\n{t[:600]}")
asyncio.run(main())
