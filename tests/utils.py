from typing import Optional
from fastapi_middleware_logger import FastAPIMiddleWareLogger
from fastapi_middleware_logger.fastapi_middleware_logger import (
    default_error_logger,
    default_logger,
)
from fastapi.testclient import TestClient
import logging
import json


def get_test_client(
    caplog,
    custom_logger: Optional[callable] = default_logger,
    custom_error_logger: Optional[callable] = default_error_logger,
):
    caplog.set_level(logging.INFO)

    app = FastAPIMiddleWareLogger(
        custom_logger=custom_logger,
        custom_error_logger=custom_error_logger,
    )

    @app.get("/")
    def get_index():
        return {"status": "ok"}

    @app.post("/some_post")
    def post_some_post(body: dict):
        return body

    @app.get("/error")
    def get_error():
        raise TypeError("Some error happened !")

    test_client = TestClient(app=app)

    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)
    caplog.clear()

    return test_client


def parse_logs(caplog):
    _, _, text = caplog.record_tuples[0]

    data = json.loads(text)

    return data
