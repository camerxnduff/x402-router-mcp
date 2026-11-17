# X402 Router paid client (Python). pip install "x402[httpx,evm]"
# Pays 0.01 USDC on Base per call (gasless EIP-3009 signature; the wallet needs a little USDC, no ETH).
# Usage: EVM_PRIVATE_KEY=0x... python paid_client.py "weather"
import asyncio, json, os, sys
from eth_account import Account
from x402 import x402Client
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

ROUTER = os.environ.get("X402_ROUTER_URL", "https://router-production-ab89.up.railway.app")

async def route_paid(q: str = "", chain: str = "Base", max_price: float | None = None, category: str | None = None) -> dict:
    """Best live x402 endpoint for a task + the full ranked list (up to 25). Costs 0.01 USDC."""
    client = x402Client()
    register_exact_evm_client(client, EthAccountSigner(Account.from_key(os.environ["EVM_PRIVATE_KEY"])))
    body = {k: v for k, v in {"q": q, "chain": chain, "max_price": max_price, "category": category}.items() if v not in (None, "")}
    async with x402HttpxClient(client) as http:   # gets the 402, signs the USDC authorization, retries
        r = await http.post(f"{ROUTER}/route/paid", json=body)
        await r.aread()
        r.raise_for_status()
        return r.json()

if __name__ == "__main__":
    print(json.dumps(asyncio.run(route_paid(" ".join(sys.argv[1:]) or "weather")), indent=1))
