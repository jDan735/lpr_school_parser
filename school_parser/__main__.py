import json
import time

import httpx
# import todoist
import webbrowser

from .config import BASE_URL
from .models import TASKS, Schedule, Task


def safe_get(*args, **kwargs) -> httpx.Response:
    try:
        return httpx.get(*args, **kwargs)
    except Exception as e:
        print("Cannot get task, wait 5 seconds ", e)
        time.sleep(5)
        return safe_get(*args, **kwargs)


def get_schedule(class_id: int) -> list[Schedule]:
    # r = safe_get(f"{BASE_URL}/api/guest/schedule?eclass={class_id}")

    # with open("schedule.json", "w", encoding="utf-8") as file:
        # file.write(r.text)

    with open("schedule.json", "r", encoding="utf-8") as file:
        text = file.read()

    return Schedule.parse_raw(text).__root__


def get_task(task_id: str) -> Task:
    r = safe_get(f"{BASE_URL}/api/guest/task?id={task_id}")
    return Task.parse_raw(r.text)


if __name__ == "__main__":
    schedule = get_schedule(48)
    md_tasks = []

    for leason in schedule:
        allowed_leasons = [
            # "математика", "алгебра", "геометрия"
        ]

        if all([not leason.name_raw.lower().startswith(x) for x in allowed_leasons]):
            continue

        for task_preview in leason.tasks:
            if task_preview.is_deployed:
                continue

            # webbrowser.open_new_tab(task_preview.url)

            task = get_task(task_preview.id)

            if task.is_deployed:
               continue

            md_tasks.append(" ".join([
                "- [ ]",
                f"{leason.date}.",
                f"{leason.name_raw}",
                f"**{task.homework_parsed[:256]}**",
                f"[на сайте]({task.url})"
            ]))

            with open("inbox.md", "a", encoding="utf-8") as f:
                f.write(md_tasks[-1] + "\n")

            with open("tasks.json", "w", encoding="UTF-8") as f:
                TASKS.append(task.id)
                f.write(json.dumps(TASKS))
