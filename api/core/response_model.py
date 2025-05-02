from pydantic import BaseModel
from typing import List, Generic, TypeVar

T = TypeVar("T")

class ErrorResponse(BaseModel):
    error: str

class SuccessResponse(BaseModel):
    message: str

class SingleResponse(BaseModel, Generic[T]):
    data: List[T]

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    data: List[T]