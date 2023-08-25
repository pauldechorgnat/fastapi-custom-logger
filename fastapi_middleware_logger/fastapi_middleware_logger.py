from fastapi import FastAPI, Response, Request
from starlette.background import BackgroundTask
from starlette.types import Message
import logging
import json


def default_logger(**kwargs):
    print(json.dumps(kwargs, indent=4))


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


def disable_loggers():
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.setLevel(level=logging.CRITICAL)
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.setLevel(level=logging.CRITICAL)
    uvicorn_access = logging.getLogger("uvicorn")
    uvicorn_access.setLevel(level=logging.CRITICAL)
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(level=logging.CRITICAL)


def add_custom_logger(
    app: FastAPI,
    custom_logger: callable = default_logger,
    disable_uvicorn_logging: bool = True,
):
    if disable_uvicorn_logging:
        disable_loggers()

    @app.middleware("http")
    async def middleware_logger(request: Request, call_next):
        request_body = await request.body()
        await set_body(request, request_body)
        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        task = BackgroundTask(
            custom_logger,
            **{
                "request_body": request_body.decode("utf-8"),
                "request_headers": dict(request.headers),
                "request_query_params": dict(request.query_params),
                "request_method": request.method,
                "request_url": str(request.url),
                "response_body": response_body.decode("utf-8"),
                "response_headers": dict(response.headers),
                "response_media_type": response.media_type,
                "response_status_code": response.status_code,
            },
        )
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=task,
        )

    return app


class FastAPIMiddleWareLogger(FastAPI):
    def __init__(
        self,
        custom_logger: callable = default_logger,
        disable_uvicorn_logger: bool = True,
        *args,
        **kwargs,
    ):
        FastAPI.__init__(self, *args, **kwargs)
        add_custom_logger(
            self,
            custom_logger=custom_logger,
            disable_uvicorn_logging=disable_uvicorn_logger,
        )
