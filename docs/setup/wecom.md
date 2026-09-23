# 企业微信 / WeCom

Provider：`wecom`

最简单的是群机器人 Webhook。

在目标企业微信群的群设置里添加群机器人，复制它生成的 Webhook URL。

GitHub Secret：

```text
WECOM_WEBHOOK_URL
```

Variable：

```text
RELAY_PROVIDER=wecom
```

也支持 `wechat-work`、`work-wechat` 别名。

Webhook URL 本身能直接向群里发消息，按 Secret 管理。

如果测试失败，优先检查 URL 是否完整、机器人是否仍在目标群，以及企业策略是否限制群机器人。
