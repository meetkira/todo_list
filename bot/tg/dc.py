from dataclasses import dataclass
from typing import List, Optional

import marshmallow
import marshmallow_dataclass


@dataclass
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    username: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: Optional[str] = None
    username: Optional[str] = None
    last_name: Optional[str] = None

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Message:
    message_id: int
    from_: MessageFrom
    chat: Chat
    text: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE


GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
SendMessageResponseSchema = marshmallow_dataclass.class_schema(SendMessageResponse)
