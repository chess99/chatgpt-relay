# ChatGPT Relay

把 ChatGPT 的计划任务/条件监控，在真正命中条件时，转发到你自己的消息渠道。**不需要 VPS、NAS 或常驻服务器。**

目前内置的第一个 provider 是 **飞书 / Lark**。仓库本身不绑定飞书：核心只负责“ChatGPT → GitHub Issue → GitHub Actions → provider”，以后可以继续增加 Telegram、企业微信、Slack、邮件或其他渠道。

## 工作原理

```text
ChatGPT 计划任务
      ↓ 条件命中
GitHub 私有 relay 仓库：创建 [relay] Issue
      ↓
GitHub Actions 托管 runner
      ↓
relay/main.py
      ↓
provider（当前：Feishu）
      ↓
你的消息渠道
```

GitHub Issues 同时保留发送历史，ChatGPT 可以用规范 URL、帖子 ID、公告 ID 等做去重。

## 当前支持

| Provider | 状态 | 认证方式 |
| --- | --- | --- |
| Feishu / Lark | ✅ 内置 | 群自定义机器人 Webhook；或企业自建应用 App ID/App Secret + chat_id |
| Telegram | ⏳ 未内置 | provider 接口已预留 |
| 企业微信 / WeCom | ⏳ 未内置 | provider 接口已预留 |
| Slack / Email / 其他 | ⏳ 未内置 | provider 接口已预留 |

扩展方式见 [docs/PROVIDERS.md](docs/PROVIDERS.md)。

## 你需要准备什么

1. 一个 GitHub 账号。
2. 一个你要使用的消息渠道；本版教程先以飞书为例。
3. ChatGPT 中可用的计划任务/自动化功能，以及 GitHub 连接。

**Secret 不要上传成 ChatGPT Source，也不要提交进 Git。** 仓库只放公开代码；真正的 Webhook、Token、Secret 放在 GitHub Actions Secrets。

## 1. 创建自己的 relay 仓库

推荐点击 GitHub 的 **Use this template** 创建仓库；Fork 也可以。

建议：
- 你自己的 relay 仓库设为 **Private**。
- 不要把 Webhook、Token、Secret 写进任何文件或 Issue。
- 仓库只给你本人或可信协作者访问。

> 模板仓库可以公开；真正带 Secrets 并接收 ChatGPT relay Issue 的用户仓库建议保持私有。

## 2. 配置 provider（本版：飞书）

Feishu provider 支持两种模式。**新用户优先用 A；已经有企业自建应用的用户可以直接用 B。**

### A. 群自定义机器人 Webhook（推荐给新用户）

在目标飞书群中添加“自定义机器人”，复制：
- Webhook URL
- 签名校验 Secret（如果开启签名校验）

推荐开启**签名校验**。Webhook URL 本身也应视为 Secret。

在仓库 **Settings → Secrets and variables → Actions → New repository secret** 添加：

| Secret | 必填 | 内容 |
| --- | --- | --- |
| `FEISHU_WEBHOOK_URL` | 是 | 自定义机器人 Webhook URL |
| `FEISHU_WEBHOOK_SECRET` | 否，但推荐 | 自定义机器人签名校验 Secret |

### B. 企业自建应用（适合已有机器人/应用的用户）

如果你已经有飞书企业自建应用，并且知道目标群的 `chat_id`，可以不创建 Webhook 机器人，改为添加：

| Secret | 必填 | 内容 |
| --- | --- | --- |
| `FEISHU_APP_ID` | 是 | 飞书应用 App ID |
| `FEISHU_APP_SECRET` | 是 | 飞书应用 App Secret |
| `FEISHU_CHAT_ID` | 是 | 目标群 chat_id |

Feishu provider 会优先使用 Webhook 模式；如果没有配置 `FEISHU_WEBHOOK_URL`，才会尝试企业自建应用模式。

> 如果旧 App Secret 曾经进入 Git 历史、聊天或其他不受控位置，建议先在飞书后台轮换，再把新 Secret 放进 GitHub Actions Secrets。

使用 GitHub 托管 runner 时，一般不要依赖固定出口 IP 白名单，因为 runner 的公网出口不是你的固定服务器。

## 3. Provider 选择

默认 provider 就是 `feishu`，因此这一版普通用户不用额外配置。

未来仓库增加其他 provider 后，可以在：

**Settings → Secrets and variables → Actions → Variables**

添加：

```text
RELAY_PROVIDER=telegram
```

或对应 provider 名称。Secret 仍然只放 Actions Secrets，不放 Variables。

## 4. 先测试 GitHub → 消息渠道

进入：

**Actions → Relay message → Run workflow**

message 填：

```text
ChatGPT Relay test
```

运行成功后，目标消息渠道应该立即收到消息。

这个测试完全不依赖 ChatGPT，适合先确认 GitHub Actions → provider 这一半链路正常。

## 5. 连接 ChatGPT 与 GitHub

在 ChatGPT 中连接 GitHub，并允许它访问你刚创建的 relay 仓库。

为了让计划任务无人值守运行，ChatGPT 在这个专用仓库里创建 relay Issue 时不能每次都卡在人工批准上。请按你能接受的最小权限原则配置 GitHub 连接；如果产品首次要求一次授权/批准，按界面完成即可。

## 6. 把 Prompt 交给 ChatGPT

打开 [PROMPT.md](PROMPT.md)，替换占位符，然后把整段复制给 ChatGPT。

你不需要自己手工创建 cron、GitHub Actions 定时器或服务器程序。Prompt 会要求 ChatGPT：
- 先验证 GitHub relay 仓库可访问
- 做一次端到端 relay 测试
- 自己建立计划任务
- 没有新信号时保持安静
- 命中条件时同时通知 ChatGPT 和外部消息渠道
- 用历史 relay Issues 去重，避免重复轰炸

## 为什么用 Issue 当 relay？

ChatGPT 的 GitHub 连接可以在已有仓库中创建 Issue，而 GitHub Actions 可以监听 `issues: opened`。因此 Issue 很适合当一个轻量、可审计的“消息队列”。

成功发送后 workflow 会自动关闭 relay Issue；closed Issues 仍然保留，既方便去重，也方便排错。

## 安全设计

- Workflow 只处理标题以 `[relay]` 开头的 Issue。
- Issue 创建者必须与仓库具有可信关联（Owner / Member / Collaborator）。
- 推荐用户自己的 relay 仓库保持 Private。
- Provider 凭据只存在 GitHub Actions Secrets。
- Sender 不会打印凭据。
- 如果 Secret 曾被提交到 Git、贴进 Issue 或公开聊天，请直接在对应服务后台轮换。

更多说明见 [SECURITY.md](SECURITY.md)。

## 本地测试

项目使用 Python 标准库，不需要第三方运行依赖：

```bash
python -m unittest discover -s tests -v
python -m py_compile relay/main.py relay/providers/feishu.py
```

## 常见问题

**Actions 里看不到 “Relay message”**

确认 workflow 已经存在于默认分支的 `.github/workflows/relay.yml`，并检查仓库 **Settings → Actions → General** 是否允许 GitHub Actions 运行。

**ChatGPT 说看不到刚创建的 relay 仓库**

如果 GitHub 连接只授权了“Selected repositories”，新建/从模板创建的仓库可能需要在 GitHub App 授权里补选，或者重新连接后授予该仓库访问权。

**创建了 `[relay]` Issue，但一直没有自动关闭**

打开仓库的 **Actions** 页面查看对应的 “Relay message” run。Issue 只有在 provider 成功返回后才会自动关闭，所以“仍然打开”通常意味着 workflow 被跳过或发送失败。

**Workflow 报缺少 provider 凭据**

检查 GitHub Actions Secrets 的名字是否完全一致。不要把真实 Secret 贴到 Issue、README 或聊天里；只确认 Secret 是否存在即可。

## 目录结构

```text
relay/
  main.py                 # 通用入口 / provider 分发
  providers/
    feishu.py             # 当前内置 provider
.github/workflows/
  relay.yml               # Issue / 手动触发 → provider
  test.yml                # CI
PROMPT.md                  # 普通用户直接复制给 ChatGPT
SECURITY.md                # Secret 与权限说明
docs/PROVIDERS.md          # 增加新渠道的约定
```
