# Security

## Secret 只放 GitHub Actions Secrets

不要把以下任何内容放进 ChatGPT Source、Git 文件、Issue、PR、日志或截图：

- Webhook URL
- Bot Token / Access Token
- App Secret
- API Token / Auth Token
- Twilio Auth Token
- 其他 provider 凭据

Webhook URL 本身也应视为 Secret，因为很多平台拿到 URL 就能直接发消息。

各 provider 使用的 Secret 名称见 [docs/PROVIDERS.md](docs/PROVIDERS.md)。

## 仓库建议

模板仓库可以公开，因为不包含凭据。

真正用于 relay 的个人仓库建议保持 **Private**，并只给本人或可信协作者访问。Workflow 还会额外检查：

- Issue 标题必须以 `[relay]` 开头；
- Issue 作者必须是 Owner / Member / Collaborator。

这是第二层保护，不替代 GitHub 仓库权限。

## 日志与错误

Provider 共享的 HTTP 层不会把请求 URL 打印到错误里，避免 Webhook URL 泄漏。Provider 也不应打印 Authorization header、Token 或 Secret。

## 凭据泄露

如果 Secret 曾经进入 Git 历史、Issue、公开聊天或日志，请直接去对应平台后台**轮换凭据**。删除最新文件不能清除旧 commit 中的值。

## 费用渠道

Twilio SMS 等渠道会产生真实费用。先在供应商侧配置预算/限额，并通过 Actions 手动测试确认目标号码后，再交给自动化使用。
