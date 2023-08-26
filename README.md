# FastAPI MiddleWare Logger

This library is a very simple tool to simplify custom formatting of logs for FastAPI.
It's almost entirely based on this [answer](https://stackoverflow.com/a/73464007) from SO.

## Usage

The design of this library is made to be very simple to use. Instead of instantiating `FastAPI`, just instatiate `FastAPIMiddleWareLogger`:

```python
from fastapi_middleware_logger.fastapi_middleware_logger import add_custom_logger
from fastapi_middleware_logger import FastAPIMiddleWareLogger
import logging
from fastapi import FastAPI


logging.basicConfig(level=logging.INFO)


app = FastAPIMiddleWareLogger()
# app = FastAPI()
# app = add_custom_logger(app)


@app.get("/")
def get_index():
    return {"status": "ok"}


@app.get("/error")
def get_error():
    raise TypeError("Some error happened !")

```
Another way to add custom loggers is to use `add_custom_logger`.

## Custom logger

If the request is handled properly, the `custom_logger` will be called.
The `custom_logger` can take the following arguments:
- `request_body`: body of the request as a **string**
- `request_headers`: headers of the request as a **dictionary**
- `request_query_params`: query parameters of the request as a **dictionary**
- `request_method`: method of the request as a **string**
- `request_url`: URL of the request as a **string**
- `response_body`: body of the response as a **string**
- `response_headers`: headers of the response as a **dictionary**
- `response_media_type`: media type of the response as a **string**
- `response_status_code`: status code of the response as an **integer**

By default, the `custom_logger` will print out all of these arguments.


## Custom error logger

If the request throws an exception, the `custom_error_logger` will be called.
The `custom_error_logger` can take the following arguments:
- `request_body`: body of the request as a **string**
- `request_headers`: headers of the request as a **dictionary**
- `request_query_params`: query parameters of the request as a **dictionary**
- `request_method`: method of the request as a **string**
- `request_url`: URL of the request as a **string**
- `error_message`: message of the exception as a **string**


Usual `uvicorn/fastapi` logs can be kept by using `disable_uvicorn_logging=False`.
This could be used to perform other operations but I have not, nor will, tested it.
