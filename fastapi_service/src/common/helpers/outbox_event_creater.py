import uuid
from typing import Optional
from uuid import UUID


def build_outbox_event(
    event_type: str,
    routing_key: str,
    video_id: UUID,
    prompt: Optional[str],
    future_video_path_in_container: str,
    extra_payload: dict,
) -> dict:
    return {
        "event_type": event_type,
        "routing_key": routing_key,
        "payload": {
            "video_id": str(video_id),
            "prompt": prompt,
            "event_id": str(uuid.uuid4()),
            "future_video_path_in_container": future_video_path_in_container,
            **extra_payload,
        },
        "processed": False,
    }
