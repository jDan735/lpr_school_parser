from pydantic import BaseModel
from .leason import Leason


class Schedule(BaseModel):
    __root__: list[Leason]
