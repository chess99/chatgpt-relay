# Twilio SMS

Provider：`twilio`，别名：`sms`

> SMS 会产生真实费用。先确认号码、地区限制和预算，再交给自动化。

官方 quickstart：
https://www.twilio.com/docs/messaging/quickstart

## 方式 A：Twilio 手机号

GitHub Secrets：

```text
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_FROM
TWILIO_TO
```

`TWILIO_FROM` / `TWILIO_TO` 建议使用 E.164 格式，例如 `+14155552671`。

## 方式 B：Messaging Service

改为：

```text
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_MESSAGING_SERVICE_SID
TWILIO_TO
```

Messaging Service 需要已经配置可用 Sender。

官方文档：
https://www.twilio.com/docs/messaging/tutorials/send-messages-with-messaging-services

## 设置 provider

```text
RELAY_PROVIDER=twilio
```

或：

```text
RELAY_PROVIDER=sms
```

先用 `Relay message` 发一条很短的测试短信。Trial 账号通常只能向已验证目标号码发送。
