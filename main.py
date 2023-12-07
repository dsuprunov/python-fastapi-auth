from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from api_v1 import router as router_v1

api_v1_prefix = '/api/v1'


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=api_v1_prefix)


@app.get('/')
def hello_index():
    return {
        'message': 'Hello index!',
    }


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
