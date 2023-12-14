from .api import api
from .auth import auth
from .admin import admin
from fastapi import APIRouter

router = APIRouter()


router.include_router(api.router)
router.include_router(admin.router)
router.include_router(auth.router)
