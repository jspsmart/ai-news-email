#!/usr/bin/env python3
# -*- coding: utf-8 -*-
f"""
每日 AI 新闻摘要 - 通过 Tavily 获取当日 AI 相关新闻 Top Any 并发送到指定邮箱
"""
import os
import smtplib
import ssl
from datetime import datetime
from pathlib import Path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import certifi
from dotenv import load_dotenv

# 解决certifi证书路径问题
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# 从脚本所在目录加载 .env，避免从其他目录运行时读不到配置
load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
TO_EMAIL = os.environ.get("TO_EMAIL", "ldk0309@163.com")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "").strip()
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD", "").strip()
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.163.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))

num = 10

def fetch_ai_news():
    f"""使用 Tavily API 搜索当日 AI新闻，返回前 {num} 条"""
    
    if not TAVILY_API_KEY:
        raise ValueError("请设置环境变量 TAVILY_API_KEY 或配置 .env")
    # 使用系统默认证书路径
    resp = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": "AI人工智能技术、软件编程方向 新闻",
            "search_depth": "advanced",
            "max_results": num,
            "include_answer": False
        },
        timeout=30,
        verify=certifi.where()
    )
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])[:num]
    return results


def build_email_body(results):
    """将搜索结果整理为邮件正文"""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"【每日 AI新闻 摘要】{date_str}", "", "=" * 50, ""]
    for i, r in enumerate(results, 1):
        title = r.get("title", "无标题")
        url = r.get("url", "")
        content = (r.get("content") or "")[:280].strip()
        if content and not content.endswith("..."):
            content = content + "..."
        lines.append(f"{i}. {title}")
        lines.append(f"   链接: {url}")
        lines.append(f"   摘要: {content}")
        lines.append("")
    return "\n".join(lines)


def send_email(body):
    """通过 SMTP 发送邮件（支持 Gmail 587/STARTTLS、163 465/SSL 等）"""
    if not FROM_EMAIL or not EMAIL_APP_PASSWORD:
        raise ValueError(
            "请设置 .env 中的 FROM_EMAIL 和 EMAIL_APP_PASSWORD（163 邮箱需在网页版 设置 -> POP3/SMTP/IMAP 中开启服务并获取授权码）"
        )
    msg = MIMEMultipart()
    msg["Subject"] = f"每日 AI新闻 Top{num} - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg.attach(MIMEText(body, "plain", "utf-8"))

    context = ssl.create_default_context()
    # Gmail 常用 587 + STARTTLS；163 等常用 465 + SSL
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as s:
            s.login(FROM_EMAIL, EMAIL_APP_PASSWORD)
            s.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls(context=context)
            s.login(FROM_EMAIL, EMAIL_APP_PASSWORD)
            s.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())


def main():
    print(f"正在获取 AI新闻 ...")
    results = fetch_ai_news()
    if not results:
        print("未获取到结果，请检查 Tavily API 或网络")
        return
    print(f"已获取 {len(results)} 条新闻，正在发送邮件到 {TO_EMAIL} ...")
    body = build_email_body(results)
    send_email(body)
    print("发送成功。")


if __name__ == "__main__":
    main()
