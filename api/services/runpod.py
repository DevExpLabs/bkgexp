import requests
from settings import settings
from schemas.runpod import RunpodResponse, RunpodResponseError


class RunpodService:
    def run(self, fileUrl: str) -> RunpodResponse:
        if settings.env == "PROD":
            return self._runpodRun(fileUrl)
        else:
            return self._localRun(fileUrl)

    def _runpodRun(self, fileUrl: str) -> RunpodResponse | RunpodResponseError:
        headers = {
            "Authorization": f"Bearer {settings.runpod_token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        body = {"input": {"fileUrl": fileUrl}}
        response = requests.post(
            settings.runpod_runsync_url, headers=headers, json=body
        ).json()

        return response

    def _localRun(self, fileUrl: str) -> RunpodResponse:
        body = {"input": {"fileUrl": fileUrl}}
        response = requests.post("http://localhost:8001/runsync", json=body).json()

        return response
