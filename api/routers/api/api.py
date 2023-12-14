from fastapi import APIRouter, Depends
from routers.api import images, stats
from routers.authentication import get_client

router = APIRouter(prefix="/api", dependencies=[Depends(get_client)])

router.include_router(images.router)
router.include_router(stats.router)
