# app/tasks/background.py
from datetime import datetime
LOG_FILE = "notifications.log"

def send_notification(username: str, task_title: str):
    """模拟发送邮件/消息：写入日志文件"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        # ✅ 保证变量名与形参一致
        f.write(
            f"[{datetime.now()}] 通知：用户 {username} 创建了任务《{task_title}》\n"
        )
