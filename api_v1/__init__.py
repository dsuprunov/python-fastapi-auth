from fastapi import APIRouter

from .auth_basic.views import router as auth_basic_router
from .auth_header.views import router as auth_header_router
from .auth_cookie.views import router as auth_cookie_router

router = APIRouter()
router.include_router(router=auth_basic_router)
router.include_router(router=auth_header_router)
router.include_router(router=auth_cookie_router)
