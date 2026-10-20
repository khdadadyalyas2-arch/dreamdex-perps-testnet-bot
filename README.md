# DreamDEX Perps Testnet Bot (MVP)

An open-source, **testnet-only** research bot scaffold for the dreamDEX Perps Builder Bounty. It includes a deterministic paper-trading loop, a transparent momentum strategy, configurable risk limits, JSONL trade logs, and a reproducible summary report. It does not custody funds or submit real orders.

> **Integration status:** This MVP currently runs against a local deterministic simulator. It is not connected to dreamDEX. Before claiming an API/SDK integration, obtain the official testnet docs and validate the adapter against the live testnet. Never use a mainnet key.

## Quick start

Requires Python 3.10+; no third-party dependencies.

```sh
python -m unittest discover -s tests -v
python run.py --bars 500 --seed 7 --out artifacts
```

Outputs `artifacts/trades.jsonl` and `artifacts/report.json`. Run the same command twice to reproduce the same results.

## Strategy

A simple moving-average crossover with an RSI guard; position size is constrained by a per-trade risk budget and maximum notional. Fees and slippage are simulated. This is a demonstration strategy, not financial advice and not evidence of profitability.

## Safety and limitations

- Simulator only; no wallet, private key, RPC transaction signing, or live order submission.
- Synthetic market data; results do not predict real performance.
- Do not describe simulated trades as testnet executions.
- A live testnet adapter should be implemented only from official dreamDEX documentation, with testnet chain-ID checks and explicit order-size limits.

## Project status

Initial MVP scaffold. The challenge submission should include a screen recording, reproducibility instructions, and genuine testnet/API feedback if obtained. See `docs/INTEGRATION.md`.
