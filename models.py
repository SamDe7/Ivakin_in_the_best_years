from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class UserContent(BaseModel):
    id: Optional[int] = None
    user_id: int
    content_type: Literal['text', 'image']
    content_data: str = Field(..., min_length=1)
    file_size: Optional[int]
    save_probability: str
    created_at: datetime = Field(default_factory=datetime.now)
    content_hash: Optional[str] = None
    chat_id: int

    @classmethod
    def get_from_telegram_message(cls, user_id: int, chat_id: int,  content_type: Literal['text', 'image'],
                                    content_data: str, save_probability: str, file_size: int = None):
        return cls(user_id=user_id,
                    chat_id=chat_id,
                    content_type=content_type,
                    content_data=content_data,
                    save_probability=save_probability,
                    file_size=file_size
                    )