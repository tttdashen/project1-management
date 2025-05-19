import re
from fastapi.testclient import TestClient
from app.main import app

def test_timer_prints(capsys):
    TestClient(app).get("/docs")
    out = capsys.readouterr().out
    # ✅ 匹配中文或英文都行，只要包含 GET /docs
    assert re.search(r"🕒 .*GET /docs.*", out)
