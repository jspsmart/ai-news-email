# 测试变量作用域问题

def fetch_ai_news():
    """模拟获取新闻"""
    num = 6
    return ["新闻1", "新闻2", "新闻3", "新闻4", "新闻5", "新闻6"]


def send_email(body):
    """模拟发送邮件"""
    # 这里会引用fetch_ai_news中的局部变量num，应该会导致NameError
    print(f"发送邮件，包含Top{num}条新闻")
    print(f"邮件内容: {body}")


def main():
    """主函数"""
    print("获取新闻...")
    results = fetch_ai_news()
    body = f"共有{len(results)}条新闻"
    print("发送邮件...")
    send_email(body)


if __name__ == "__main__":
    main()
