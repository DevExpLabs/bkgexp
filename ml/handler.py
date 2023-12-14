from time import time, strftime
from PIL import Image
from io import BytesIO
from uuid import uuid4
import boto3, botocore, os
import runpodUtils as rutils
from model.model import Model
from urllib.parse import urlparse


class Handler:
    def __init__(self, model: Model) -> None:
        self.model = model

    def get_source_image(self, file_url: str):
        response, image_download_time = rutils.downloadImage(file_url)
        sourceImage = rutils.getImageFromResponse(response)
        return sourceImage, image_download_time

    def __call__(self, event):
        fileUrl = event["input"]["fileUrl"]
        try:
            sourceImage, image_download_time = self.get_source_image(fileUrl)
        except Exception as e:
            return {"error": f"{e}"}

        try:
            main_operation_time = time()

            _, cutout, timings = self.model.run(sourceImage)
            resultImg = Image.fromarray(cutout)

            bts = BytesIO()
            resultImg.save(bts, format="webp")
            bts.seek(0)

            main_operation_time = time() - main_operation_time
            timings["main_operation_time"] = main_operation_time
            timings["image_download_time"] = image_download_time
            print(f"Main Operation run time: {main_operation_time}[s]")

            upload_url = self.upload_image(event["id"], bts)

            return {
                "imageUrl": upload_url,
                "timings": timings,
            }
        except Exception as e:
            print(f"Backgroud cut handler failed with: {e}")
            return {"error": f"Backgroud cut handler failed with: {e}"}

    def extract_region_from_url(self, endpoint_url: str):
        """
        Extracts the region from the endpoint URL.
        """
        parsed_url = urlparse(endpoint_url)
        # AWS/backblaze S3-like URL
        if ".s3." in endpoint_url:
            return endpoint_url.split(".s3.")[1].split(".")[0]

        # DigitalOcean Spaces-like URL
        if parsed_url.netloc.endswith(".digitaloceanspaces.com"):
            return endpoint_url.split(".")[1].split(".digitaloceanspaces.com")[0]

        return None

    def get_client(self):
        """
        Returns a boto3 client and transfer config for the bucket.
        """
        session = boto3.session.Session()
        config = botocore.config.Config(
            signature_version="s3v4", retries={"max_attempts": 3, "mode": "standard"}
        )

        endpoint_url = os.environ.get("BUCKET_ENDPOINT_URL", None)
        access_key_id = os.environ.get("BUCKET_ACCESS_KEY_ID", None)
        secret_access_key = os.environ.get("BUCKET_SECRET_ACCESS_KEY", None)

        if endpoint_url and access_key_id and secret_access_key:
            region = self.extract_region_from_url(endpoint_url)
            return session.client(
                "s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                config=config,
                region_name=region,
            )

        return None

    def upload_image(
        self,
        job_id: int,
        image_location: bytes,
        result_index=0,
        results_list=None,
        file_extension: str = "webp",
    ):
        """
        Upload image to bucket storage.
        """
        image_name = str(uuid4())[:8]
        boto_client = self.get_client()

        if boto_client is None:
            # Save the output to a file
            print("No bucket endpoint set, saving to disk folder 'simulated_uploaded'")
            print("If this is a live endpoint, please reference the following:")
            print(
                "https://github.com/runpod/runpod-python/blob/main/docs/serverless/worker-utils.md"
            )

            os.makedirs("simulated_uploaded", exist_ok=True)
            sim_upload_location = f"simulated_uploaded/{image_name}.{file_extension}"
            with Image.open(image_location) as img, open(
                sim_upload_location, "wb"
            ) as file_output:
                img.save(file_output, format=img.format)

            if results_list is not None:
                results_list[result_index] = sim_upload_location

            return sim_upload_location

        with Image.open(image_location) as img:
            output = BytesIO()
            img.save(output, format=img.format)
            output.seek(0)

            bucket = strftime("%m-%y")
            boto_client.put_object(
                Bucket=f"{bucket}",
                Key=f"{job_id}/{image_name}.{file_extension}",
                Body=output.getvalue(),
                ContentType=f"image/{file_extension}",
            )

            presigned_url = boto_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": f"{bucket}",
                    "Key": f"{job_id}/{image_name}.{file_extension}",
                },
                ExpiresIn=60,  # 60 seconds
            )

            if results_list is not None:
                results_list[result_index] = presigned_url

            return presigned_url
