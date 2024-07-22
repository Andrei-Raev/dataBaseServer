from typing import Optional

from pydantic import BaseModel


class Achievement(BaseModel):
    id: int = None
    title: str
    description: Optional[str] = None
    static_image: Optional[str] = None
    animated_image: Optional[str] = None

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int = None
    external_id: str
    achievements_history: Optional[list[Achievement]] = None

    class Config:
        orm_mode = True
        from_attributes = True


class Card(BaseModel):
    id: int
    title: str
    description: str
    extended_description: str
    created_at: str
    type: int
    rewardPoints: int
    rewardAchievement: int
    activator: str
    progress_type: int

    class Config:
        orm_mode = True


class CardProgress(BaseModel):
    id: int
    card: int
    user: int
    progress: str
    is_finished: bool
    finished_at: str

    class Config:
        orm_mode = True


class OperationType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class OperationHistory(BaseModel):
    id: int
    user: int
    type: int
    data: str
    date: str

    class Config:
        orm_mode = True


class Type(BaseModel):
    id: int
    name: str
    description: str
    color: str

    class Config:
        orm_mode = True
