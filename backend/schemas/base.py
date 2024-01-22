from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class Base(BaseModel):
    id: int
