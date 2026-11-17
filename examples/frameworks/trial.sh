#!/bin/sh
# Free trial of X402 Router's paid route: 3 free calls per wallet per day, no payment needed.
# Put your own wallet address in X-402-Trial (EVM 0x... or Solana base58). Nothing is signed or charged.
ROUTER="${X402_ROUTER_URL:-https://router-production-ab89.up.railway.app}"
WALLET="${WALLET:-0xYourWalletAddressHere000000000000000000}"
curl -s -D - -X POST "$ROUTER/route/paid" \
  -H 'content-type: application/json' \
  -H "X-402-Trial: $WALLET" \
  -d '{"q":"weather","chain":"Base"}'
# 200 + headers  X-402-Trial: true  X-402-Trial-Remaining: N  -> same full ranked answer as a paid call.
# When the trial is used up you get the normal 402 (PAYMENT-REQUIRED) plus X-402-Trial-Remaining: 0;
# from then on pay 0.01 USDC per call with any x402 client (see paid_client.py / paid-client.ts).
