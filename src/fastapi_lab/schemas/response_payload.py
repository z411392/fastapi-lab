from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class ResponsePayload(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: Optional[T] = None
