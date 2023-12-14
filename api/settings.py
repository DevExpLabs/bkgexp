from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    image_format: str = "webp"
    env: str
    region_name: str
    endpoint_url: str
    bucket_name: str
    bucket_path: str
    runpod_runsync_url: str
    runpod_token: str
    should_upload_to_s3: bool
    aws_access_key_id: str
    aws_secret_access_key: str
    admin_api_key: str = "de4e2dfebb803b4c0808104959daa960166a4657e39a3d295c67e9b48174b4a2"  # 6221c617-1380-4912-88eb-ba737be2b8ce
    database_url: str
    port: int = 8000


settings = Settings()
