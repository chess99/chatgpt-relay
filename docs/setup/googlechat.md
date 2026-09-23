# Google Chat

Provider：`googlechat`

本项目使用 Google Chat Space 的 Incoming Webhook，适合外部系统单向通知。

在浏览器打开目标 Space：

**Apps & integrations → Add webhooks**

创建后复制 Webhook URL。

官方文档：
https://developers.google.com/workspace/chat/quickstart/webhooks

Google 官方说明，Webhook URL 中含有需要保密的 token；而且某些 Workspace 管理员会禁止普通用户添加 Webhook。

GitHub Secret：

```text
GOOGLE_CHAT_WEBHOOK_URL
```

Variable：

```text
RELAY_PROVIDER=googlechat
```

也支持 `gchat` 和 `google-chat` 别名。

最后运行 `Relay message` 测试。
