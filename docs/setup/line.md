# LINE

Provider：`line`

LINE 比 Webhook 渠道稍复杂，需要 **LINE Official Account + Messaging API channel + 目标 ID**。

## 1. 启用 Messaging API

先创建 LINE Official Account，再启用 Messaging API。

官方文档：
https://developers.line.biz/en/docs/messaging-api/getting-started/

## 2. 获取 Channel Access Token

在对应 Messaging API channel 中获取 Channel Access Token。

官方文档：
https://developers.line.biz/en/docs/basics/channel-access-token/

GitHub Secret：

```text
LINE_CHANNEL_ACCESS_TOKEN
```

## 3. 获取目标 ID

还需要：

```text
LINE_TO_ID
```

它可以是 Messaging API 支持的 user / group / room 目标 ID，通常来自 LINE webhook event。

因此如果你还没有任何 webhook 接收方式，LINE 不算最适合新手的第一个 provider；Telegram、Discord、Feishu、Slack、企业微信更省事。

## 4. GitHub 配置

Secrets：

```text
LINE_CHANNEL_ACCESS_TOKEN
LINE_TO_ID
```

Variable：

```text
RELAY_PROVIDER=line
```

最后运行 `Relay message` 测试。
