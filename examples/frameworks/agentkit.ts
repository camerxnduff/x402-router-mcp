// Coinbase AgentKit + X402 Router. npm i @coinbase/agentkit viem   (run with tsx; tested with @coinbase/agentkit 0.10.4)
// Note: strict `tsc` can flag viem type mismatches/depth here (AgentKit pins its own viem); the code runs fine under tsx.
// AgentKit's built-in x402 action provider pays x402 v2 endpoints with your wallet. It gives the agent the actions
// make_http_request, retry_http_request_with_x402, make_http_request_with_x402 and discover_x402_services.
import { AgentKit, ViemWalletProvider, x402ActionProvider } from "@coinbase/agentkit";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const walletProvider = new ViemWalletProvider(createWalletClient({
  account: privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`), chain: base, transport: http(),
}));
const agentKit = await AgentKit.from({ walletProvider, actionProviders: [x402ActionProvider()] });
// (AgentKit's main branch adds x402ActionProvider({ registeredServices: [...], maxPaymentUsdc }) to whitelist services
//  and cap spend; use it once it is in a release.)

// Direct call, no LLM: the provider reads the 402, signs 0.01 USDC on Base and retries.
const provider = x402ActionProvider();
console.log(await provider.makeHttpRequestWithX402(walletProvider, {
  url: "https://router-production-ab89.up.railway.app/route/paid", method: "POST",
  headers: { "content-type": "application/json" }, body: { q: "weather", chain: "Base" },
} as any));
// With an LLM: pass agentKit to a framework extension, e.g. getLangChainTools(agentKit) from @coinbase/agentkit-langchain.
