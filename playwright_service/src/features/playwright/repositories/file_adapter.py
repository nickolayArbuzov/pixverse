import aiofiles
import os
from fastapi import UploadFile
from typing import AsyncGenerator


class FileAdapter:
    def __init__(self, base_path: str = "/shared"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    async def save_download(self, filename: str, download_obj) -> str:
        path = os.path.join(self.base_path, filename)
        await download_obj.save_as(path)
        return path

    async def read_file(self, filename: str) -> AsyncGenerator[bytes, None]:
        path = os.path.join(self.base_path, filename)
        async with aiofiles.open(path, "rb") as in_file:
            while chunk := await in_file.read(1024 * 1024):
                yield chunk
