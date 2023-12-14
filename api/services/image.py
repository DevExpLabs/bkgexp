from io import BytesIO
from uuid import uuid4
import boto3, os, botocore
from settings import settings
from fastapi import UploadFile
import utils.image as imageUtils
from .runpod import RunpodService
from schemas.runpod import RunpodResponse, RunpodResponseError


class ImageService:
    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(
            "s3",
            endpoint_url=settings.endpoint_url,
            config=botocore.config.Config(s3={"addressing_style": "virtual"}),
            region_name=settings.region_name,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    def remove_background(
        self, uploadedImages: list[UploadFile], runpodService: RunpodService
    ) -> list[RunpodResponse | RunpodResponseError]:
        runpodResponses = []
        for uploadedImage in uploadedImages:
            imageBts = imageUtils.getBytesFromImageFile(uploadedImage.file)
            uploadUrl = self._uploadImage(imageBts)
            runpodResponse = runpodService.run(uploadUrl)
            runpodResponses.append(runpodResponse)

        return runpodResponses

    def _uploadImage(self, imageBts: BytesIO) -> str:
        if settings.env == "PROD" or settings.should_upload_to_s3:
            return self._s3Upload(imageBts)
        else:
            return self._localUpload(imageBts)

    def _s3Upload(self, imageBts: BytesIO) -> str:
        key = f"{settings.bucket_path}/{str(uuid4())[:8]}.{settings.image_format}"
        self.client.put_object(
            Bucket=settings.bucket_name,
            Key=key,
            Body=imageBts.getvalue(),
            ACL="private",
            ContentType=f"image/{settings.image_format}",
        )

        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.bucket_name, "Key": key},
            ExpiresIn=60,  # 60 seconds
        )

    def _localUpload(self, imageBts: BytesIO) -> str:
        os.makedirs("simulated_uploaded", exist_ok=True)
        key = f"{os.getcwd()}/simulated_uploaded/{str(uuid4())[:8]}.{settings.image_format}"
        with open(key, "wb") as simulated_upload:
            simulated_upload.write(imageBts.getvalue())

        return key
