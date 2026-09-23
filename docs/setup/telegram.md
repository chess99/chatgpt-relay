# Telegram

Provider：`telegram`

需要：

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

## 1. 创建 Bot

打开 Telegram 官方 **@BotFather**，发送 `/newbot`，按提示完成创建。BotFather 会返回 Bot Token。

官方文档：
https://core.telegram.org/bots/features

## 2. 让 bot 进入目标聊天

私聊：打开 bot，点 Start 并发送一条消息。

群组：把 bot 加入目标群，再在群里发一条消息或 @ 一下 bot。

## 3. 找 Chat ID

在自己电脑终端临时运行：

```bash
read -s TELEGRAM_BOT_TOKEN
export TELEGRAM_BOT_TOKEN
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates"
unset TELEGRAM_BOT_TOKEN
```

不要把 Token 直接写进命令行。返回 JSON 中的 `message.chat.id` 就是 `TELEGRAM_CHAT_ID`。群组 ID 为负数很常见。

## 4. 填 GitHub

Secrets：

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

Variable：

```text
RELAY_PROVIDER=telegram
```

最后运行 `Relay message` 测试。
