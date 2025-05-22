from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.pixverse_adapter import PixverseAdapter
from src.dependencies import get_db
from src.features.video.usecases.command import (
    Text2VideoUseCase,
    Text2VideoCommand,
    Image2VideoUseCase,
    Image2VideoCommand,
)
from src.features.video.usecases.query import (
    GetStatusGenerateUseCase,
    GetStatusGenerateQuery,
)
from src.features.video.repositories import VideoCommandRepository, VideoQueryRepository

from src.features.video.video_schema import CreateVideo, ResponseVideo
from src.features.video.video_swagger import GetStatusGenerateDoc

router = APIRouter()


def get_command_repo(db: AsyncSession = Depends(get_db)) -> VideoCommandRepository:
    return VideoCommandRepository(db)


def get_query_repo(db: AsyncSession = Depends(get_db)) -> VideoQueryRepository:
    return VideoQueryRepository(db)


def get_pixverse_adapter() -> PixverseAdapter:
    return PixverseAdapter(
        base_url="https://app-api.pixverse.ai",
        api_key="your-key",
        ai_trace_id="Ai-trace-id",
    )


@router.post("/text_2_video", response_model=ResponseVideo)
async def text_2_video(
    video: CreateVideo,
    repo: VideoCommandRepository = Depends(get_command_repo),
    pixverse_adapter: PixverseAdapter = Depends(get_pixverse_adapter),
):
    command = Text2VideoCommand(video=video)
    use_case = Text2VideoUseCase(repo, pixverse_adapter)
    return await use_case.execute(command)


@router.post("/image_2_video", response_model=ResponseVideo)
async def image_2_video(
    video: CreateVideo,
    repo: VideoCommandRepository = Depends(get_command_repo),
    pixverse_adapter: PixverseAdapter = Depends(get_pixverse_adapter),
):
    command = Image2VideoCommand(video=video)
    use_case = Image2VideoUseCase(repo, pixverse_adapter)
    return await use_case.execute(command)


@router.get("/status/{video_id}", responses=GetStatusGenerateDoc)
async def GetStatusGenerate(
    video_id: int,
    repo: VideoQueryRepository = Depends(get_query_repo),
    pixverse_adapter: PixverseAdapter = Depends(get_pixverse_adapter),
):
    query = GetStatusGenerateQuery(video_id=video_id)
    use_case = GetStatusGenerateUseCase(repo, pixverse_adapter)
    return await use_case.execute(query)
