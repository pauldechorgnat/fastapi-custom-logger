from fastapi_custom_logger import FastAPIMiddleWareLogger
import logging


def my_custom_logger(response_status_code, **kwargs):
    if response_status_code != 200:
        logging.error("Some error happened")


app = FastAPIMiddleWareLogger(custom_logger=my_custom_logger)


@app.get("/")
def get_index():
    return {"status": "ok"}
