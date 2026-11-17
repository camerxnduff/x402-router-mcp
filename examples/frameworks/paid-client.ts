// X402 Router paid client (TypeScript, Node 20+). npm i @x402/fetch @x402/evm viem
// Pays 0.01 USDC on Base per call (gasless EIP-3009 signature; the wallet needs a little USDC, no ETH).
// Usage (ESM: "type": "module" in package.json, or save as .mts): EVM_PRIVATE_KEY=0x... npx tsx paid-client.ts "weather"
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const ROUTER = process.env.X402_ROUTER_URL ?? "https://router-production-ab89.up.railway.app";
const client = new x402Client();
registerExactEvmScheme(client, { signer: privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`) });
const pay = wrapFetchWithPayment(fetch, client);   // gets the 402, signs the USDC authorization, retries

export async function routePaid(q: string, chain = "Base", max_price?: number) {
  const res = await pay(`${ROUTER}/route/paid`, {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ q, chain, ...(max_price !== undefined ? { max_price } : {}) }),
  });
  if (!res.ok) throw new Error(`router answered ${res.status}`);
  return res.json();   // { best, ranked[], target_url, price, ... }
}

console.log(JSON.stringify(await routePaid(process.argv.slice(2).join(" ") || "weather"), null, 1));
