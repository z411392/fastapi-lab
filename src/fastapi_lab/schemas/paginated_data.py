from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    page: int
    page_size: int
    total_pages: int
    total_items: int


class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    pagination: Pagination
