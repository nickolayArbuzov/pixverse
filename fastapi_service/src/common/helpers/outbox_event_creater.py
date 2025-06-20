import uuid
from typing import Optional
from uuid import UUID


def build_outbox_event(
    event_type: str,
    routing_key: str,
    video_id: UUID,
    prompt: Optional[str],
    extra_payload: Optional[dict] = None,
) -> dict:
    extra_payload = extra_payload or {}
    return {
        "event_type": event_type,
        "routing_key": routing_key,
        "payload": {
            "video_id": str(video_id),
            "prompt": prompt,
            "event_id": str(uuid.uuid4()),
            **extra_payload,
        },
        "processed": False,
    }
