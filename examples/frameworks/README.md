# Framework examples for X402 Router

Copy-paste clients for the router's paid route (`POST /route/paid`, 0.01 USDC on Base via x402 v2). Each guide is also on the web at
https://router-production-ab89.up.railway.app/integrations.

| File | Stack | Notes |
|---|---|---|
| `paid_client.py` | Python, `x402[httpx,evm]` | `route_paid()` helper used by the LangChain and CrewAI tools |
| `paid-client.ts` | TypeScript, `@x402/fetch` + `@x402/evm` + `viem` | ESM (`"type": "module"` or `.mts`) |
| `langchain_tool.py` | LangChain (`langchain_core.tools.tool`) | free top-3 tool + paid full-ranking tool |
| `crewai_tool.py` | CrewAI (`crewai.tools.tool`) | same two tools |
| `agentkit.ts` | Coinbase AgentKit `x402ActionProvider` | uses your AgentKit wallet |

Test status (17 Nov 2026): x402 2.28.0, @x402/fetch 2.31.0, langchain-core 1.8.1, crewai 1.15.41 and @coinbase/agentkit 0.10.4 were run against a local
replay of the router's live 402. Each produced a valid 0.01 USDC payment on eip155:8453 to the router's payTo. The signed payments were captured
locally and never sent. The LLM agent wiring in the comments was not executed. Use a dedicated low-balance wallet (`EVM_PRIVATE_KEY`).
