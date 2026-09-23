# Discord

Provider：`discord`

## 推荐：Channel Webhook

在目标服务器进入：

**Server Settings → Integrations → Webhooks**

创建 Webhook、选择目标频道并复制 Webhook URL。

官方文档：
https://discord.com/developers/docs/resources/webhook

GitHub Secret：

```text
DISCORD_WEBHOOK_URL
```

Variable：

```text
RELAY_PROVIDER=discord
```

Webhook URL 本身就是 Secret。

## 已有 Bot

也可以配置：

```text
DISCORD_BOT_TOKEN
DISCORD_CHANNEL_ID
```

Bot 需要在目标服务器里，并有目标频道的查看和发消息权限。若同时配置 Webhook，relay 优先用 Webhook。

最后运行 `Relay message` 测试。
