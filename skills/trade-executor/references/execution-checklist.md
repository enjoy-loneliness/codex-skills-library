# Execution Checklist

Use this checklist for live, paper, or simulated order execution.

## Required Ticket Fields

- Account or venue
- Environment: live, paper, sandbox, simulation, or backtest
- Instrument symbol exactly as accepted by the venue
- Asset class and contract type
- Side: buy, sell, short, cover, open, close, reduce, or hedge
- Quantity or sizing formula
- Order type: market, limit, stop, stop-limit, trailing, TWAP, VWAP, iceberg, or bracket
- Time in force
- Limit, stop, trigger, or protection prices when applicable
- Reduce-only, post-only, close-only, margin mode, leverage, and position side when applicable
- Client order ID or idempotency key when supported

## Pre-Trade Checks

- Latest bid, ask, last price, mark price, and timestamp
- Market status and trading session
- Tick size, lot size, step size, minimum notional, and price bands
- Buying power, cash, margin, borrow availability, and unsettled funds
- Existing position, open orders, and pending cancels
- Estimated notional, fees, slippage, and margin impact
- Max position size, leverage, concentration, and loss-limit rules
- Derivatives multiplier, expiry, settlement asset, funding, and liquidation buffer
- Corporate actions, halts, hard-to-borrow status, or venue restrictions where relevant

## Confirmation Ticket Format

Show the user:

```text
Account/Venue:
Environment:
Action:
Instrument:
Quantity:
Order Type:
Limit/Stop:
Time in Force:
Flags:
Estimated Notional:
Estimated Fees/Slippage:
Position After Fill:
Main Risk:
```

Require explicit confirmation if and only if the next step submits, modifies, or cancels a live order.

## API Handling

- Use official SDK methods when available.
- Redact secrets, signatures, cookies, and account tokens in logs and chat.
- Prefer idempotent submissions with client order IDs.
- Treat network timeouts as unknown state until the order is queried by client order ID or server order ID.
- After any timeout, rate-limit, or retryable error, query open orders and fills before retrying.
- Never retry a live order blindly if the first request may have reached the venue.

## Failure Triage

For rejected orders, collect:

- Exact venue error code and message
- Request payload with secrets redacted
- Instrument metadata used for rounding
- Account permissions and environment
- Available balance or margin at submission time
- Open orders and position at submission time
- Whether the request was create, replace, cancel, or close

Common causes: symbol mismatch, market closed, insufficient funds, size below minimum, invalid tick or lot step, post-only would cross, reduce-only would increase exposure, leverage too high, missing trading permission, stale timestamp, duplicate client order ID, or sandbox/live environment mismatch.
