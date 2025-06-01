import uuid
from typing import Optional
from uuid import UUID


def build_outbox_event(
    event_type: str,
    routing_key: str,
    video_id: UUID,
    status: str,
    extra_payload: dict,
) -> dict:
    return {
        "event_type": event_type,
        "routing_key": routing_key,
        "payload": {
            "video_id": str(video_id),
            "event_id": str(uuid.uuid4()),
            "status": status,
            **extra_payload,
        },
        "processed": False,
    }
