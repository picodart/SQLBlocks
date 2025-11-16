from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, Tuple

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def ok(cls, data: T) -> "Result[T]":
        return cls(success=True, data=data)
    
    @classmethod
    def err(cls, error: str) -> "Result[T]":
        return cls(success=False, error=error)

@dataclass
class BasicSQLBlock:
    name: str 
    sql: str
    depends: Optional[Tuple[str, ...]] = None

    def __post_init__(self):
        self.depends = self.depends or ()




