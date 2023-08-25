from typing import Optional
from fastapi_middleware_logger import FastAPIMiddleWareLogger
from fastapi.testclient import TestClient
import logging


def get_application(
    custom_logger: Optional[callable] = None,
):
    if custom_logger:
        app = FastAPIMiddleWareLogger(custom_logger=custom_logger)
    else:
        app = FastAPIMiddleWareLogger()

    @app.get("/")
    def get_index():
        return {"status": "ok"}

    @app.post("/some_post")
    def post_some_post(body):
        return body

    @app.get("/error")
    def get_error():
        raise TypeError("Some error happened !")

    test_client = TestClient(app=app)

    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)

    return test_client
