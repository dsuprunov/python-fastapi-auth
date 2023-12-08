from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
import uvicorn

from auth_basic.views import router as auth_basic_router
from auth_header.views import router as auth_header_router
from auth_cookie.views import router as auth_cookie_router

router = APIRouter()
router.include_router(router=auth_basic_router, prefix='/auth')
router.include_router(router=auth_header_router, prefix='/auth')
router.include_router(router=auth_cookie_router, prefix='/auth')


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router, prefix='')


@app.get('/')
def index():
    return {
        'message': 'Hello World!',
    }


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
