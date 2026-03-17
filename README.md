# 每日 AI 新闻邮件摘要

每天自动获取当日 AI 相关新闻 Top10，并发送到 163 邮箱（收件、发件均为 163）。

## 环境要求

- Python 3.7+
- 163 邮箱：`xxxxxx@163.com`（收件与发件同一账号）

## 163 邮箱如何获取授权码

发件必须使用「授权码」，不能使用登录密码。按下面步骤操作一次即可。

### 步骤一：登录 163 邮箱网页版

1. 浏览器打开 **https://mail.163.com**
2. 用你的 163 账号登录（如 `asigned email`）

### 步骤二：进入 POP3/SMTP/IMAP 设置

1. 登录后点击页面顶部的 **「设置」**（或右上角齿轮图标）
2. 在左侧菜单选择 **「POP3/SMTP/IMAP」**（或「POP3/SMTP/IMAP 服务」）

### 步骤三：开启 SMTP 服务并获取授权码

1. 找到 **「IMAP/SMTP 服务」** 或 **「POP3/SMTP 服务」**
2. 点击 **「开启」**（若已开启可跳过）
3. 按页面提示完成**手机验证**（发短信验证码到绑定手机）
4. 验证通过后，页面会提示你**设置授权码**：
   - 有的版本是「新增授权密码」或「生成授权码」
   - 自己设一个**授权码**（建议记在密码管理器里），**这不是登录密码**，仅用于 SMTP 发信
5. 把生成的或你设置的**授权码**复制下来（只显示一次，务必保存）

### 步骤四：填到项目里

编辑项目目录下的 `.env` 文件，把授权码填进去：

```env
EMAIL_APP_PASSWORD=你刚才获取的163授权码
```

保存后即可用脚本发信。

---

**小结**：163 网页版 → 设置 → POP3/SMTP/IMAP → 开启 IMAP/SMTP 服务 → 手机验证 → 设置/获取授权码 → 把授权码填到 `.env` 的 `EMAIL_APP_PASSWORD`。

## 快速开始

### 1. 安装依赖

```bash
cd /Users/yourName/ai-news-digest
pip3 install -r requirements.txt
```

### 2. 配置授权码

按上面「163 邮箱如何获取授权码」完成操作后，在 `.env` 中填写：

- `EMAIL_APP_PASSWORD=你的163授权码`

收件、发件邮箱和 SMTP 已默认写好（`xxxxxx@163.com`、`smtp.163.com:465`），无需改。

### 3. 手动运行一次测试

```bash
python3 ai_news_digest.py
```

成功后会向 `xxxxxx@163.com` 发送一封「每日 AI 新闻 Top10」邮件。

### 4. 每天 8:30 自动发送（macOS）

```bash
crontab -e
```

在末尾添加一行：

```
30 8 * * * cd /Users/yourName/ai-news-email && /usr/bin/python3 ai_news_digest.py >> /Users/yourName/ai-news-digest/cron.log 2>&1
```

保存后，每天 8:30 会自动跑脚本并写日志到 `cron.log`。

## 文件说明

| 文件 | 说明 |
|------|------|
| `ai_news_digest.py` | 主脚本：拉取 Tavily AI 新闻 + 发邮件 |
| `.env` | 本地配置（API Key、邮箱、163 授权码），勿提交 Git |
| `requirements.txt` | Python 依赖 |

## 注意事项

- `.env` 已加入 `.gitignore`，请勿把包含授权码的 `.env` 上传到公开仓库。
- 163 发件必须用「授权码」，不能用登录密码；授权码仅在开启 SMTP 时设置，请妥善保存。
