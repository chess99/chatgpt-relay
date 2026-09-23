# ChatGPT Relay

把 ChatGPT 的计划任务/条件监控，在真正命中条件时，转发到你自己的消息渠道。**不需要 VPS、NAS 或常驻服务器。**

目前内置的第一个 provider 是 **飞书 / Lark 自定义机器人**。仓库本身不绑定飞书：核心只负责“ChatGPT → GitHub Issue → GitHub Actions → provider”，以后可以继续增加 Telegram、企业微信、Slack、邮件或其他渠道。

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

| Provider | 状态 | 凭据 |
| --- | --- | --- |
| Feishu / Lark 自定义机器人 | ✅ 内置 | `FEISHU_WEBHOOK_URL`、可选 `FEISHU_WEBHOOK_SECRET` |
| Telegram | ⏳ 未内置 | provider 接口已预留 |
| 企业微信 / WeCom | ⏳ 未内置 | provider 接口已预留 |
| Slack / Email / 其他 | ⏳ 未内置 | provider 接口已预留 |

扩展方式见 [docs/PROVIDERS.md](docs/PROVIDERS.md)。

## 你需要准备什么

1. 一个 GitHub 账号。
2. 一个你要使用的消息渠道；本版教程先以飞书群“自定义机器人”为例。
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

在目标飞书群中添加“自定义机器人”，复制：
- Webhook URL
- 签名校验 Secret（如果开启签名校验）

推荐开启**签名校验**。Webhook URL 本身也应视为 Secret。

使用 GitHub 托管 runner 时，一般不要依赖固定出口 IP 白名单，因为 runner 的公网出口不是你的固定服务器。

## 3. 添加 GitHub Actions Secrets

打开你自己的 relay 仓库：

**Settings → Secrets and variables → Actions → New repository secret**

飞书 provider 使用：

| Secret | 必填 | 内容 |
| --- | --- | --- |
| `FEISHU_WEBHOOK_URL` | 是 | 飞书自定义机器人 Webhook URL |
| `FEISHU_WEBHOOK_SECRET` | 否，但推荐 | 飞书机器人“签名校验”的 Secret |

默认 provider 就是 `feishu`，因此普通用户不用额外配置。未来如果仓库增加其他 provider，可在 **Actions → Variables** 设置 `RELAY_PROVIDER` 切换。

## 4. 先测试 GitHub → 消息渠道

进入：

**Actions → Relay message → Run workflow**

message 填：

```text
ChatGPT Relay test
```

运行成功后，飞书群应该立即收到消息。

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
