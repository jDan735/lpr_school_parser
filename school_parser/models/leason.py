from datetime import datetime
from pydantic import BaseModel
from .task import TaskPreview

import pendulum as pdl


class LeasonInfo(BaseModel):
    id: int
    name: str


class Leason(BaseModel):
    leason: LeasonInfo
    tasks: list[TaskPreview]

    year: int
    month: int
    day: int

    week_day: int

    @property
    def id(self) -> int:
        return self.leason.id

    @property
    def date(self) -> str:
        return f"{self.day:02}.{self.month:02}"

    @property
    def name_raw(self) -> str:
        return self.leason.name

    @property
    def name_fixed(self) -> str:
        return self.name_raw.replace("(", "<").replace(")", ">")
