from fastapi.testclient import TestClient
import logging
import json
from fastapi_custom_logger.fastapi_custom_logger import FastAPIMiddleWareLogger


def read_standard_output(text):
    lines = text.split("\n")

    return "\n".join(lines[1:])


def test_logger(caplog):
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)
    caplog.set_level(logging.INFO)
    app = FastAPIMiddleWareLogger(disable_uvicorn_logger=True)

    @app.get("/")
    def get_index():
        return {"status": "ok"}

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(read_standard_output(caplog.text))
    assert data
