from fastapi.testclient import TestClient
import logging
import json
from fastapi_middleware_logger.fastapi_middleware_logger import FastAPIMiddleWareLogger


def test_get_index(caplog):
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)

    caplog.set_level(logging.INFO)

    app = FastAPIMiddleWareLogger(disable_uvicorn_logger=True)

    @app.get("/")
    def get_index():
        return {"status": "ok"}

    client = TestClient(app)
    caplog.clear()

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    _, _, text = caplog.record_tuples[0]

    data = json.loads(text)

    assert data["request_body"] == ""
    assert data["request_headers"]["host"] == "testserver"
    assert data["request_query_params"] == {}
    assert data["request_method"] == "GET"
    assert data["request_url"] == f"{client.base_url}/"

    assert json.loads(data["response_body"]) == {"status": "ok"}
    assert data["response_headers"]["content-type"] == "application/json"

    assert data["response_status_code"] == 200


def test_get_index_with_error(caplog):
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)

    caplog.set_level(logging.INFO)

    app = FastAPIMiddleWareLogger(disable_uvicorn_logger=True)

    @app.get("/")
    def get_index():
        raise TypeError
        return {"status": "ok"}

    client = TestClient(app)
    caplog.clear()

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    _, _, text = caplog.record_tuples[0]

    data = json.loads(text)

    assert data["request_body"] == ""
    assert data["request_headers"]["host"] == "testserver"
    assert data["request_query_params"] == {}
    assert data["request_method"] == "GET"
    assert data["request_url"] == f"{client.base_url}/"


def test_get_index_with_query_parameters(caplog):
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)

    caplog.set_level(logging.INFO)

    app = FastAPIMiddleWareLogger(disable_uvicorn_logger=True)

    @app.get("/")
    def get_index():
        return {"status": "ok"}

    client = TestClient(app)
    caplog.clear()

    response = client.get("/", params={"hello": "world"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    _, _, text = caplog.record_tuples[0]

    data = json.loads(text)

    assert data["request_body"] == ""
    assert data["request_headers"]["host"] == "testserver"
    assert data["request_query_params"] == {"hello": "world"}
    assert data["request_method"] == "GET"
    assert data["request_url"] == f"{client.base_url}/?hello=world"

    assert json.loads(data["response_body"]) == {"status": "ok"}
    assert data["response_headers"]["content-type"] == "application/json"

    assert data["response_status_code"] == 200


def test_post_index_with_body(caplog):
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)

    caplog.set_level(logging.INFO)

    app = FastAPIMiddleWareLogger(disable_uvicorn_logger=True)

    @app.get("/")
    def get_index():
        return {"status": "ok"}

    client = TestClient(app)
    caplog.clear()

    response = client.post("/", json={"hello": "world"})
    assert response.status_code == 405

    _, _, text = caplog.record_tuples[0]

    data = json.loads(text)

    assert json.loads(data["request_body"]) == {"hello": "world"}
    assert data["request_headers"]["host"] == "testserver"
    assert data["request_query_params"] == {}
    assert data["request_method"] == "POST"
    assert data["request_url"] == f"{client.base_url}/"

    assert data["response_status_code"] == 405


def test_wrong_url(caplog):
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)

    caplog.set_level(logging.INFO)

    app = FastAPIMiddleWareLogger(disable_uvicorn_logger=True)

    @app.get("/")
    def get_index():
        return {"status": "ok"}

    client = TestClient(app)
    caplog.clear()

    response = client.get("/wrong_url")
    assert response.status_code == 404

    _, _, text = caplog.record_tuples[0]

    data = json.loads(text)

    assert data["request_body"] == ""
    assert data["request_headers"]["host"] == "testserver"
    assert data["request_query_params"] == {}
    assert data["request_method"] == "GET"
    assert data["request_url"] == f"{client.base_url}/wrong_url"

    assert data["response_status_code"] == 404


def test_get_index_with_custom_logger(caplog):
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)

    caplog.set_level(logging.INFO)

    def custom_logger(**kwargs):
        logging.info(json.dumps({"status": "ok"}))

    app = FastAPIMiddleWareLogger(
        custom_logger=custom_logger,
        disable_uvicorn_logger=True,
    )

    @app.get("/")
    def get_index():
        return {"status": "ok"}

    client = TestClient(app)
    caplog.clear()

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    _, _, text = caplog.record_tuples[0]

    data = json.loads(text)

    assert data == {"status": "ok"}


def test_get_index_with_custom_loader_with_error(caplog):
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(level=logging.CRITICAL)

    caplog.set_level(logging.INFO)

    def custom_logger(**kwargs):
        logging.info(json.dumps({"status": "ok"}))

    app = FastAPIMiddleWareLogger(
        custom_logger=custom_logger,
        disable_uvicorn_logger=True,
    )

    @app.get("/")
    def get_index():
        raise TypeError
        return {"status": "ok"}

    client = TestClient(app)
    caplog.clear()

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    _, _, text = caplog.record_tuples[0]

    data = json.loads(text)

    assert data["request_body"] == ""
    assert data["request_headers"]["host"] == "testserver"
    assert data["request_query_params"] == {}
    assert data["request_method"] == "GET"
    assert data["request_url"] == f"{client.base_url}/"
