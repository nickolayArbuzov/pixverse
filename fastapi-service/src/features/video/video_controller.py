from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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
from src.features.outbox.repositories import OutboxCommandRepository

from src.features.video.video_schema import Video, ResponseVideo

router = APIRouter()


@router.post("/text_2_video", response_model=ResponseVideo)
async def text_2_video(
    video: Video,
    db: AsyncSession = Depends(get_db),
):
    video_repo = VideoCommandRepository(db)
    outbox_repo = OutboxCommandRepository(db)

    command = Text2VideoCommand(video=video)
    use_case = Text2VideoUseCase(
        video_repository=video_repo,
        outbox_repository=outbox_repo,
    )
    return await use_case.execute(command)


@router.post("/image_2_video", response_model=ResponseVideo)
async def image_2_video(
    video: Video,
    db: AsyncSession = Depends(get_db),
):
    video_repo = VideoCommandRepository(db)
    outbox_repo = OutboxCommandRepository(db)
    command = Image2VideoCommand(video=video)
    use_case = Image2VideoUseCase(
        video_repository=video_repo,
        outbox_repository=outbox_repo,
    )
    return await use_case.execute(command)


@router.get("/status/{video_id}")
async def GetStatusGenerate(
    video_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = VideoQueryRepository(db)
    query = GetStatusGenerateQuery(video_id=video_id)
    use_case = GetStatusGenerateUseCase(repo)
    return await use_case.execute(query)
