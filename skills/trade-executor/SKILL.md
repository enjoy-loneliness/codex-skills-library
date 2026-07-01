---
name: trade-executor
description: 执行交易下单。Use when the user asks Codex to place, execute, or submit a trade order through the configured n8n webhook.
---

# Trade Executor

## Instructions

首先完整读取 `references/execution-checklist.md`。调用用户已配置的交易执行 webhook
前，必须遵守其中的订单票据、风险检查、幂等和超时处理要求。公开分享本 skill 时不要写入
真实 URL 或 API Key。

所有请求默认是 `simulation` 或 `paper`，不得自行推断为 `live`。用户没有明确指定环境
时，先询问；不得让 webhook 的默认配置替用户选择 live。

```text
POST <TRADE_WEBHOOK_URL>
```

Headers:

```text
X-API-KEY: <TRADE_WEBHOOK_API_KEY>
```

Body:

```json
{
  "symbol": "BTCUSDT",
  "side": "buy",
  "amount": 100
}
```

下单前必须确认完整订单票据，至少包括：

- `account/venue`
- `environment`：`live`、`paper`、`sandbox` 或 `simulation`
- `symbol`
- `side`
- `amount` 或明确的仓位计算方式
- `order type`
- 适用的价格、时效、杠杆、保证金模式、`reduce-only` / `post-only`
- 预计名义价值、费用、滑点、成交后仓位和主要风险

如果缺少参数，先询问用户。

如果下一步会创建、修改或撤销 live 订单，先向用户展示最终不可变订单票据，并针对这张
票据取得一次明确确认；未确认时只能 dry-run，不得调用 live webhook。

调用完成后，返回 n8n 响应结果。网络超时或不确定响应不代表失败，也不得盲目重试；先按
client order ID 或服务端 order ID 查询订单、成交和持仓状态。
