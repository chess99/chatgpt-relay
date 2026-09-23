# Provider 扩展约定

`chatgpt-relay` 的核心不绑定任何消息平台。`relay/main.py` 只负责选择 provider，并把最终消息交给 provider。

当前内置：

- `feishu` → `relay/providers/feishu.py`
  - 群自定义机器人 Webhook
  - 企业自建应用 App API

未来可以增加：

- `telegram`
- `wecom`
- `slack`
- `email`
- 任何有 HTTP API / Webhook 的渠道

## Provider 接口

每个 provider 模块实现：

```python
def send(message: str) -> None:
    ...
```

Provider 自己从环境变量读取所需凭据，成功时返回 `None`，失败时抛出异常。不要把 Secret 作为命令行参数，也不要打印 Secret。

同一个 provider 可以支持多种认证方式。例如 Feishu provider 会优先使用 Webhook；如果没有配置 Webhook，则尝试 App ID/App Secret + chat_id。

然后在 `relay/main.py` 的 provider registry 中注册：

```python
PROVIDERS = {
    "feishu": feishu.send,
    "telegram": telegram.send,
}
```

## GitHub Actions 配置

通用 workflow 使用仓库变量：

- `RELAY_PROVIDER`

未设置时默认 `feishu`。

新增 provider 时，把该 provider 需要的 GitHub Actions Secrets 映射为同名环境变量即可。不要把真实 Secret 写进 workflow 文件，也不要尝试从 Issue 正文传递 Secret。

## 安全要求

新增 provider 必须：

1. 不把 Secret 写入源码、Issue、日志或测试 fixture。
2. 使用 GitHub Actions Secrets 注入凭据。
3. 对外部 HTTP 请求设置超时。
4. 对服务端错误做有限长度的非敏感错误输出。
5. 给签名、载荷生成和配置选择逻辑增加离线单元测试。
6. 不要因为一个 provider 失败就回退到另一个未明确配置的渠道。
