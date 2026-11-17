# LangChain tool for X402 Router. pip install langchain "x402[httpx,evm]" httpx   (+ your model's provider package)
# Put paid_client.py (from /examples) next to this file.
import httpx
from langchain_core.tools import tool
from paid_client import ROUTER, route_paid

@tool
def find_x402_api_free(task: str, chain: str = "Base") -> dict:
    """Free: best live x402 (pay-per-call) API for a task, plus the top 3 matches with prices."""
    return httpx.post(f"{ROUTER}/route", json={"q": task, "chain": chain}, timeout=30).json()

@tool
async def find_x402_api_ranked(task: str, chain: str = "Base", max_price: float = 0.05) -> dict:
    """Paid, 0.01 USDC: full ranked list (up to 25) of live x402 APIs for a task with latency, reliability,
    price and payTo, plus a ready-to-pay best pick. Use when the free top 3 is not enough."""
    return await route_paid(task, chain, max_price)

# from langchain.agents import create_agent
# agent = create_agent(model="claude-sonnet-4-6", tools=[find_x402_api_free, find_x402_api_ranked])
# result = await agent.ainvoke({"messages": [{"role": "user", "content": "Find a working weather API I can pay per call on Base"}]})
