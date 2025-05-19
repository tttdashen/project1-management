import requests, time, pprint
from pathlib import Path

BASE = "http://127.0.0.1:8000"
params = {"title": "写报告", "username": "ai模型"}

print("→ 发送 POST 请求 …")
r = requests.post(f"{BASE}/tasks/create", params=params)

print("状态码:", r.status_code)
pprint.pprint(r.json(), width=60)

print("→ 等后台任务写日志 …")
time.sleep(0.2)  # 等 200 ms

log = Path("notifications.log")
if log.exists():
    print("\n✅ 日志内容：")
    print(log.read_text(encoding="utf-8"))
else:
    print("\n❌ 未生成日志文件！")
