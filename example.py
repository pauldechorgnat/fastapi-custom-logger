from fastapi_middleware_logger.fastapi_middleware_logger import add_custom_logger
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)


# app = FastAPIMiddleWareLogger()
app = FastAPI()
app = add_custom_logger(app)


@app.get("/")
def get_index():
    return {"status": "ok"}


@app.post("/some_post")
def post_some_post(body):
    return body


@app.get("/error")
def get_error():
    raise TypeError("Some error happened !")
