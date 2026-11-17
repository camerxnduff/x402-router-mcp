# CrewAI tool for X402 Router. pip install crewai "x402[httpx,evm]" httpx
# Put paid_client.py (from /examples) next to this file.
import httpx
from crewai.tools import tool
from paid_client import ROUTER, route_paid

@tool("Find x402 API (free)")
def find_x402_api_free(task: str, chain: str = "Base") -> dict:
    """Free: best live x402 (pay-per-call) API for a task, plus the top 3 matches with prices."""
    return httpx.post(f"{ROUTER}/route", json={"q": task, "chain": chain}, timeout=30).json()

@tool("Find x402 API (ranked, 0.01 USDC)")
async def find_x402_api_ranked(task: str, chain: str = "Base", max_price: float = 0.05) -> dict:
    """Paid, 0.01 USDC: full ranked list (up to 25) of live x402 APIs for a task with latency, reliability,
    price and payTo, plus a ready-to-pay best pick."""
    return await route_paid(task, chain, max_price)

# from crewai import Agent
# scout = Agent(role="API scout", goal="Find a reliable paid API for the task", backstory="Knows the x402 ecosystem",
#               tools=[find_x402_api_free, find_x402_api_ranked])
