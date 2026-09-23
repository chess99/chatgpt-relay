# Security

## 不要把 Secret 放进 ChatGPT Source 或 Git

不要提交任何 provider 的 Webhook URL、签名 Secret、Bot Token、App Secret、API Token 或其他凭据。

对当前 Feishu provider，根据你选择的模式，只把对应值存进 **GitHub Actions repository secrets**：

### Webhook 模式

- `FEISHU_WEBHOOK_URL`
- `FEISHU_WEBHOOK_SECRET`（启用签名校验时）

Webhook URL 本身也应视为 Secret。

### 企业自建应用模式

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_CHAT_ID`

其中 `FEISHU_APP_SECRET` 必须按 Secret 管理；`chat_id` 虽然通常不等同于密码，也不建议公开散播。

## 推荐的仓库边界

模板仓库可以公开，因为模板中没有凭据。

真正用于 relay、配置了 GitHub Actions Secrets 的个人仓库推荐保持 **Private**。Workflow 还会检查：

- Issue 标题必须以 `[relay]` 开头；
- Issue 作者必须与仓库具有 Owner / Member / Collaborator 关联。

这不是用来替代仓库权限控制，而是第二层保护。

## 凭据泄露怎么办

如果凭据曾经：

- 提交到 Git；
- 粘贴进 GitHub Issue；
- 粘贴进公开聊天；
- 出现在日志或截图；

请直接去对应 provider 后台**轮换凭据**。只删除当前文件不能清除 Git 历史中的旧值。

## GitHub Actions 日志

Provider 实现不应输出 Secret。错误信息也应尽量只包含 HTTP 状态、服务端非敏感错误码和简短消息。

新增 provider 时请遵守同样原则，详见 [docs/PROVIDERS.md](docs/PROVIDERS.md)。
