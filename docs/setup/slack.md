# Slack

Provider：`slack`

## 推荐：Incoming Webhook

Slack 官方流程：

1. 创建 Slack App。
2. 打开 **Incoming Webhooks**。
3. 启用 Incoming Webhooks。
4. 点击 **Add New Webhook to Workspace**。
5. 选择目标频道并授权。
6. 复制 Webhook URL。

官方文档：
https://api.slack.com/messaging/webhooks

GitHub Secret：

```text
SLACK_WEBHOOK_URL
```

Variable：

```text
RELAY_PROVIDER=slack
```

Slack 明确把 Webhook URL 视为 Secret，不要提交进 Git。

## 已有 Bot

也可以使用：

```text
SLACK_BOT_TOKEN
SLACK_CHANNEL_ID
```

Bot 必须有发送消息权限并已加入目标频道。若同时配置 Webhook，relay 优先用 Webhook。
