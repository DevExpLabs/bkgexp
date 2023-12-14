from typing import Annotated
from schemas.client import Client
from dependencies.db import get_db
from sqlalchemy.orm import Session
from services.image import ImageService
from routers.authentication import get_client
from fastapi import APIRouter, UploadFile, Depends
from dependencies.imageFilesValidator import ImageFilesValidator
from dependencies.backgroundAccounting import BackgroundAccounting
from services.runpod import RunpodService, RunpodResponse, RunpodResponseError


router = APIRouter(prefix="/images", tags=["images"])
imageFilesValidator = ImageFilesValidator()


@router.post("/remove_background")
def remove_background(
    images: Annotated[list[UploadFile], Depends(imageFilesValidator)],
    imageService: Annotated[ImageService, Depends()],
    runpodService: Annotated[RunpodService, Depends()],
    client: Annotated[Client, Depends(get_client)],
    db: Annotated[Session, Depends(get_db)],
    accounting: Annotated[BackgroundAccounting, Depends(BackgroundAccounting)],
) -> list[RunpodResponse | RunpodResponseError]:
    bkgRmResults = imageService.remove_background(images, runpodService)
    accounting.run(db, client, bkgRmResults)

    return bkgRmResults


# ce11f0fb-2bb8-48aa-b813-7fd4bd56a00e
