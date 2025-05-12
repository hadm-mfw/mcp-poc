import uvicorn

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logger = logging.getLogger("uvicorn")

from sse.router import starlette_app

if __name__ == "__main__":
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000)
