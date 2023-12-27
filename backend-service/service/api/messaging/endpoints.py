import json

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Annotated, Optional, List

from starlette.responses import Response

from service.api.authorization.utils import validate_token
from service.api.messaging.models import MessageInput, MessageOutput
from service.api.messaging.utils import validate_message, map_to_output_message
from service.repository.messaging_repo import MessagingRepository

messages_router = APIRouter()


@messages_router.post('/{advert_id}/add')
def add_message(
        advert_id: int,
        user_id: Annotated[int, Depends(validate_token)],
        message_input: MessageInput
):
    if not user_id:
        raise HTTPException(status_code=403, detail="Unregistered users cannot send messages")

    validate_message(message_input)

    repo = MessagingRepository()

    repo.post_message(advert_id, user_id, message_input)

    return Response(status_code=200, content=json.dumps({"detail": "Message successfully sent"}))


@messages_router.get('/{advert_id}')
def fetch_messages(
        advert_id: int,
        user_id: Annotated[int, Depends(validate_token)],
        page: Annotated[int, Query(gt=0, le=100)] = 1,
        page_size: Annotated[int, Query(gt=0, le=100)] = 5
) -> List[MessageOutput]:
    repo = MessagingRepository()

    db_messages = repo.get_messages(advert_id, page, page_size)

    output_messages = []

    for db_message in db_messages:
        output_messages.append(map_to_output_message(db_message))

    return output_messages
