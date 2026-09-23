# Provider 指南

`chatgpt-relay` 只做一件事：把 ChatGPT 触发的消息，从 GitHub Actions 单向投递到外部渠道。

设计借鉴了 OpenClaw 的 channel 分层思路：**核心不理解各平台凭据和 API；每个 provider 自己负责配置、限长、认证和错误处理。** 我们没有复制 OpenClaw 的实现代码，也没有引入它的 Gateway/常驻连接层。

## 已内置

| Provider | `RELAY_PROVIDER` | GitHub Actions Secrets |
| --- | --- | --- |
| Feishu / Lark | `feishu` | Webhook: `FEISHU_WEBHOOK_URL`, 可选 `FEISHU_WEBHOOK_SECRET`; 或 App: `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_CHAT_ID` |
| Telegram | `telegram` | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| Discord | `discord` | 推荐 `DISCORD_WEBHOOK_URL`; 或 `DISCORD_BOT_TOKEN`, `DISCORD_CHANNEL_ID` |
| Slack | `slack` | 推荐 `SLACK_WEBHOOK_URL`; 或 `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID` |
| Google Chat | `googlechat` | `GOOGLE_CHAT_WEBHOOK_URL` |
| LINE | `line` | `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_TO_ID` |
| 企业微信 / WeCom | `wecom` | `WECOM_WEBHOOK_URL` |
| Twilio SMS | `twilio` / `sms` | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_TO`，以及 `TWILIO_FROM` 或 `TWILIO_MESSAGING_SERVICE_SID` |

## 为什么没有把 OpenClaw 的所有渠道都搬进来？

OpenClaw 是长期在线 Gateway，能保存连接状态、处理入站事件、二维码登录和本地桥接。GitHub-hosted relay 是短生命周期、纯 outbound runner。

因此以下类型**不适合**本项目当前模型：

- iMessage：依赖已登录 Mac、本地 Messages 数据库 / bridge。
- WhatsApp：需要二维码配对和持久会话状态。
- Signal：通常依赖长期可用的 signal-cli 注册状态。
- 微信个人号 / 二维码机器人：依赖扫码登录和持久状态。
- IRC / Matrix / Mattermost 等：虽然能做纯 outbound，但更适合有完整账户会话或长期连接的客户端；后续有需求再加。
- 语音电话：可以像 Twilio SMS 一样做，但涉及更高费用和电话流程，暂不默认内置。

我们的原则是：**只有“GitHub Actions 启动后，凭几个 Secrets 就能安全地完成一次发送”的渠道，才优先内置。**

## Provider 接口

每个 provider 模块只需要实现：

```python
def send(message: str) -> None:
    ...
```

核心通过 `relay/providers/__init__.py` 的 registry 解析 provider。新增 provider 时：

1. 建立 `relay/providers/<name>.py`。
2. 只从环境变量读取配置，不读取仓库文件里的凭据。
3. 使用 `relay.http` 发 HTTP 请求。
4. 使用 `relay.text.chunk_text` 适配平台限长。
5. 在 registry 中注册 canonical name 和必要 alias。
6. 把 Secrets 映射加入 `.github/workflows/relay.yml`。
7. 增加离线单元测试和 README 配置说明。

## 安全约束

- 不把 Secret 作为 CLI 参数。
- 不在错误信息里打印 Webhook URL、Token、Authorization header。
- Webhook URL 本身按 Secret 对待。
- 外部请求必须设置超时。
- 不自动回退到另一个 provider；配错就明确失败。
- 一个 relay Issue 成功投递后才自动关闭，失败时保留为 open，方便排查。
