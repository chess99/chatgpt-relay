# 渠道配置指南

面向普通用户：先选一个渠道，按对应文档配置 GitHub Actions Secrets，再运行一次 `Relay message` 测试。

| 渠道 | 难度 | 指南 |
| --- | --- | --- |
| Feishu / Lark | 低 | [feishu.md](feishu.md) |
| Telegram | 低 | [telegram.md](telegram.md) |
| Discord | 低 | [discord.md](discord.md) |
| Slack | 低 | [slack.md](slack.md) |
| Google Chat | 低-中 | [googlechat.md](googlechat.md) |
| 企业微信 / WeCom | 低 | [wecom.md](wecom.md) |
| LINE | 中 | [line.md](line.md) |
| Twilio SMS | 中 | [twilio.md](twilio.md) |

## 通用步骤

1. 在目标聊天工具里创建 bot / webhook / app。
2. 把凭据填到 relay 仓库的 **Settings → Secrets and variables → Actions → Secrets**。
3. 在 **Actions → Variables** 设置 `RELAY_PROVIDER`。
4. 打开 **Actions → Relay message → Run workflow** 发测试消息。
5. 成功后，把仓库根目录 [PROMPT.md](../../PROMPT.md) 复制给 ChatGPT。

不要把 Webhook、Token、App Secret 放进 ChatGPT 对话、Issue、PR、README、代码或截图。Webhook URL 本身通常也等同于 Secret。
