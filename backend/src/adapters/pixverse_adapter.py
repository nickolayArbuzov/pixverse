import httpx
from typing import Any, Dict


class PixverseAdapter:
    def __init__(self, base_url: str, api_key: str, ai_trace_id: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {"API-KEY": api_key, "Ai-trace-id": ai_trace_id}

    async def upload_image(self, file_path: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as file:
                files = {"file": (file_path, file, "image/jpeg")}
                response = await client.post(
                    f"{self.base_url}/openapi/v2/image/upload",
                    headers=self.headers,
                    files=files,
                )
            response.raise_for_status()
            return response.json()

    async def generate_text_to_video(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/openapi/v2/video/text/generate",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def generate_image_to_video(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/openapi/v2/video/img/generate",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def get_video_generation_status(self, task_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/openapi/v2/video/result/{task_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
