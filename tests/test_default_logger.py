import logging
import pytest
import json
from utils import get_test_client, parse_logs


def test_get_index_default_logger(caplog):
    client = get_test_client(caplog=caplog)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    data = parse_logs(caplog)

    assert data["request_body"] == ""
    assert data["request_headers"] == dict(response.request.headers)
    assert data["request_query_params"] == {}
    assert data["request_method"] == response.request.method
    assert data["request_url"] == response.request.url

    assert json.loads(data["response_body"]) == {"status": "ok"}
    assert data["response_headers"]["content-type"] == "application/json"

    assert data["response_status_code"] == 200


def test_get_error_default_logger(caplog):
    client = get_test_client(caplog=caplog)

    with pytest.raises(TypeError):
        client.get(
            "/error",
        )

    data = parse_logs(caplog)

    assert data["request_body"] == ""
    assert data["request_query_params"] == {}
    assert data["request_method"] == "GET"
    assert data["request_url"] == f"{client.base_url}/error"

    assert data["error_message"] == "Some error happened !"


def test_post_some_post_default_logger(caplog):
    client = get_test_client(caplog=caplog)

    response = client.post("/some_post", json={"body": "ok"})

    assert response.status_code == 200
    assert response.json() == {"body": "ok"}

    data = parse_logs(caplog)

    assert json.loads(data["request_body"]) == {"body": "ok"}
    assert data["request_headers"] == dict(response.request.headers)
    assert data["request_query_params"] == {}
    assert data["request_method"] == response.request.method
    assert data["request_url"] == response.request.url

    assert json.loads(data["response_body"]) == {"body": "ok"}
    assert data["response_headers"]["content-type"] == "application/json"

    assert data["response_status_code"] == 200


def test_get_index_custom_logger(caplog):
    def my_custom_logger(response_status_code, **kwargs):
        logging.info(json.dumps({"response_status_code": response_status_code}))

    client = get_test_client(
        caplog=caplog,
        custom_logger=my_custom_logger,
    )

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    data = parse_logs(caplog)

    assert data == {"response_status_code": 200}


def test_post_some_post_custom_logger(caplog):
    def my_custom_logger(response_status_code, **kwargs):
        logging.info(json.dumps({"response_status_code": response_status_code}))

    client = get_test_client(
        caplog=caplog,
        custom_logger=my_custom_logger,
    )

    response = client.post("/some_post", json={"body": "ok"})

    assert response.status_code == 200
    assert response.json() == {"body": "ok"}

    data = parse_logs(caplog)

    assert data == {"response_status_code": 200}


def test_get_error_custom_logger(caplog):
    def my_custom_error_logger(error_message, **kwargs):
        logging.info(json.dumps({"error_message": error_message}))

    client = get_test_client(
        caplog=caplog,
        custom_error_logger=my_custom_error_logger,
    )
    with pytest.raises(TypeError):
        client.get("/error")

    data = parse_logs(caplog)

    assert data == {"error_message": "Some error happened !"}
