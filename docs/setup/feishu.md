# Feishu / Lark

Provider：`feishu`

## 推荐：群自定义机器人 Webhook

在目标群设置中添加“自定义机器人”，复制 Webhook URL；如果启用签名校验，再复制签名 Secret。

GitHub Actions Secrets：

```text
FEISHU_WEBHOOK_URL
FEISHU_WEBHOOK_SECRET   # 仅启用签名校验时
```

Actions Variable：

```text
RELAY_PROVIDER=feishu
```

然后在 **Actions → Relay message → Run workflow** 发送测试消息。

## 已有企业自建应用

也可以不用 Webhook，配置：

```text
FEISHU_APP_ID
FEISHU_APP_SECRET
FEISHU_CHAT_ID
```

如果两套都存在，relay 优先使用 Webhook。

如果旧 App Secret 曾进入 Git 历史、聊天或截图，请先在飞书后台轮换。
