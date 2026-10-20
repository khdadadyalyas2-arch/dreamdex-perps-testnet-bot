# dreamDEX Testnet Integration: checklist

The current MVP is intentionally a local simulator. Do not claim testnet integration until each item below is verified.

1. Obtain the official dreamDEX Perps API/SDK docs and Somnia testnet chain ID/RPC from the event page or organizers.
2. Confirm current endpoints, auth model, available markets, order types, and test-USDSO faucet rules.
3. Implement an `Exchange` adapter with market-data reads first. Add strict testnet chain-ID/environment checks; fail closed if the configured network is not the documented testnet.
4. Add order submission only after dry-run tests. Enforce max order notional, leverage <= 1x, one-position limit, and explicit user opt-in. Never accept or log seed phrases/private keys.
5. Test error cases: stale prices, rejected orders, rate limits, duplicate requests, partial fills, and disconnects.
6. Compare order IDs and fills against the official explorer/UI and retain reproducible logs with secrets redacted.
7. Ask organizers to confirm that the implementation and reports comply with bounty rules.

No API details have been guessed or fabricated in this repository.
