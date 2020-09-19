from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass
class ResultWithData(Generic[T]):
    data: T
    is_error: bool
    message: str


def get_result_with_data(data: T) -> ResultWithData[T]:
    return ResultWithData(data=data, is_error=False, message="")


def get_result_with_error(error: str) -> ResultWithData[T]:
    return ResultWithData(data=None, is_error=True, message=error)

