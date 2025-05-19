# tests/test_background.py
import time
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.tasks import background

client = TestClient(app)

def test_background_writes_log(tmp_path):
    # 修改日志路径到 tmp_path，避免污染项目目录
    background.LOG_FILE = str(tmp_path / "notifications.log")

    r = client.post("/tasks/create?title=单元测试&username=user1")
    assert r.status_code == 200

    time.sleep(0.05)
    log = Path(background.LOG_FILE)
    assert log.exists() and "user1" in log.read_text(encoding="utf-8")
