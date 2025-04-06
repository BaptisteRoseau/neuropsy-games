from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Material(Enum):
    VISUAL = 1
    VERBAL = 2
    TACTILE = 3
    AUDITORY = 4


class CognitiveCategory(BaseModel):
    id: Optional[int] = None
    name: str


class CognitiveFunction(BaseModel):
    id: Optional[int] = None
    name: str


class Game(BaseModel):
    id: Optional[int] = None
    title: str
    description: str = ""
    image: Optional[str] = None
    materials: list[Material] = []
    categories: list[tuple[CognitiveCategory, int]]
    functions: list[tuple[CognitiveFunction, int]]
