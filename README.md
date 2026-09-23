# ChatGPT Relay

把 ChatGPT 的计划任务/条件监控，在真正命中条件时，转发到你自己的消息渠道。**不需要 VPS、NAS 或常驻服务器。**

```text
ChatGPT 计划任务 / 条件监控
        ↓ 命中
GitHub 私有 relay 仓库：创建 [relay] Issue
        ↓
GitHub Actions
        ↓
provider
        ↓
飞书 / Telegram / Discord / Slack / Google Chat / LINE / 企业微信 / SMS
```

## 已支持渠道

| 渠道 | Provider | 最省事的接法 |
| --- | --- | --- |
| Feishu / Lark | `feishu` | 群自定义机器人 Webhook |
| Telegram | `telegram` | BotFather token + chat ID |
| Discord | `discord` | Channel webhook |
| Slack | `slack` | Incoming webhook |
| Google Chat | `googlechat` | Space incoming webhook |
| LINE | `line` | Messaging API access token + 目标 ID |
| 企业微信 / WeCom | `wecom` | 群机器人 webhook |
| SMS | `twilio` | Twilio 账号 + 发送/接收号码 |

Feishu、Discord、Slack 还支持更完整的 App/Bot API 模式。所有 provider 与 Secret 说明见 [docs/PROVIDERS.md](docs/PROVIDERS.md)。

这个架构参考了 OpenClaw 的“channel 独立封装”思路，但只实现适合 GitHub Actions 的**无服务器单向通知层**。哪些 OpenClaw 渠道不适合这种模型，见 [docs/OPENCLAW-NOTES.md](docs/OPENCLAW-NOTES.md)。

## 普通用户只需要做 4 件事

### 1. 从模板创建自己的仓库

建议使用 **Use this template**，并把你自己的 relay 仓库设成 **Private**。

模板仓库本身可以公开；真正配置了 Secrets、接收 ChatGPT relay Issue 的仓库建议保持私有。

### 2. 选择消息渠道，填写 Secrets

打开：

**Settings → Secrets and variables → Actions**

按 [docs/PROVIDERS.md](docs/PROVIDERS.md) 中你选择的 provider 填对应 Secrets。

然后在：

**Settings → Secrets and variables → Actions → Variables**

新建：

```text
RELAY_PROVIDER=telegram
```

把 `telegram` 换成你的 provider。未设置时默认 `feishu`。

> 不要把 Webhook、Token、App Secret 上传成 ChatGPT Source，也不要提交进 Git。Webhook URL 本身也按 Secret 对待。

### 3. 手动测试一次渠道

进入：

**Actions → Relay message → Run workflow**

输入：

```text
ChatGPT Relay test
```

也可以在 provider 输入框临时指定某个 provider，而不改仓库变量。

成功后，你的目标渠道应该收到消息。

### 4. 把 PROMPT.md 复制给 ChatGPT

打开 [PROMPT.md](PROMPT.md)，替换监控目标等占位符，整段交给 ChatGPT。

Prompt 会要求 ChatGPT：

- 自己确认 relay 仓库权限；
- 自己创建一次 `[relay]` 测试 Issue；
- 自己检查是否被 Action 成功处理；
- 自己创建计划任务；
- 没有新信号时保持安静；
- 真正命中时，同时通知 ChatGPT 和你的外部渠道；
- 用历史 closed/open relay Issues 去重。

**用户不用自己写 cron，也不用自己搭服务器。**

## Relay Issue 协议

ChatGPT 需要创建：

```text
Title: [relay] <简短标题>
Body:  要转发的完整消息
```

Workflow 只接受：

- 标题以 `[relay]` 开头；
- Issue 作者是仓库 Owner / Member / Collaborator。

provider 成功后 Issue 自动关闭；失败时保持 open，方便排查。closed Issues 也是天然的发送历史和去重记录。

## 目录结构

```text
relay/
  main.py
  http.py
  text.py
  providers/
    feishu.py
    telegram.py
    discord.py
    slack.py
    googlechat.py
    line.py
    wecom.py
    twilio.py
.github/workflows/
  relay.yml
  test.yml
PROMPT.md
SECURITY.md
docs/
  PROVIDERS.md
  OPENCLAW-NOTES.md
```

## 开发与测试

运行时只使用 Python 标准库：

```bash
python -m unittest discover -s tests -v
python -m compileall -q relay tests
```

## 常见问题

**ChatGPT 看不到新建的 relay 仓库**

如果 GitHub 连接只授权 Selected repositories，需要在 GitHub App 授权里把新仓库补进去。

**创建了 `[relay]` Issue 但没有自动关闭**

打开 Actions 看 “Relay message” run。只有 provider 成功后才会关闭 Issue。

**Action 报缺少配置**

只检查对应 Secret 名称是否存在；不要把真实值贴到 Issue、README 或聊天里。

**某个平台为什么没支持？**

如果它需要常驻登录态、本地设备桥接或二维码状态，它通常不适合 GitHub-hosted 一次性 runner。见 [docs/OPENCLAW-NOTES.md](docs/OPENCLAW-NOTES.md)。
