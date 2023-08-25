# FastAPI MiddleWare Logger

This library is a very simple tool to simplify custom formatting of logs for FastAPI.
It's almost entirely based on this [answer](https://stackoverflow.com/a/73464007) from SO.

## Usage

The design of this library is made to be very simple to use. Instead of instantiating `FastAPI`, just instatiate `FastAPIMiddleWareLogger`:

```python
from fastapi_json_logger import FastAPIMiddleWareLogger

app = FastAPIMiddleWareLogger()

@app.get("/")
def get_index():
    return {"status": "ok"}

```

You can change the logger by providing a `custom_logger` function:

```python

from fastapi_json_logger import FastAPIMiddleWareLogger

def my_custom_logger(response_status_code, **kwargs):
    if response_status_code != 200:
        logging.error("Some error happened")


app = FastAPIMiddleWareLogger(custom_logger=my_custom_logger)

@app.get("/")
def get_index():
    return {"status": "ok"}

```

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

Usual `uvicorn/fastapi` logs can be kept by using `disable_uvicorn_logging=False`.
This could be used to perform other operations but I have not, nor will, tested it.
