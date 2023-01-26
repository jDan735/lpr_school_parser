from pydantic import BaseModel

from ..config import BASE_URL
import json
# from tghtml import TgHTML


class TaskPreview(BaseModel):
    id: str
    name: str

    @property
    def url(self) -> str:
        return f"{BASE_URL}/task/{self.id}"

    @property
    def is_deployed(self) -> bool:
        return self.id in TASKS


class Homework(BaseModel):
    id: str
    descr: str = None


try:
    with open("tasks.json", encoding="utf-8") as f:
        TASKS = json.loads(f.read())
except FileNotFoundError:
    TASKS = []


class Task(TaskPreview):
    homework: Homework = None

    @property
    def homework_str(self) -> str | None:
        if self.homework is None or self.homework.descr is None:
            return None

        return None

        return self.homework.descr

    @property
    def homework_parsed(self) -> str:
        return (self.homework_str or '').replace('\n', '  ')
