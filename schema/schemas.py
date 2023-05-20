'''
Description: 
Author: colin gao
Date: 2023-05-17 15:54:12
LastEditTime: 2023-05-17 16:43:13
'''
"""Schemas for the chat app."""
from pydantic import BaseModel, validator


class ChatItem(BaseModel):
    text: str
    history: list=[]


class ChatResponse(BaseModel):
    """Chat response schema."""

    sender: str
    message: str
    type: str

    @validator("sender")
    def sender_must_be_bot_or_you(cls, v):
        if v not in ["bot", "you"]:
            raise ValueError("sender must be bot or you")
        return v

    @validator("type")
    def validate_message_type(cls, v):
        if v not in ["start", "stream", "end", "error", "info"]:
            raise ValueError("type must be start, stream or end")
        return v
