from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_tasks(database: Path) -> list[dict]:
    if not database.exists():
        return []
    return json.loads(database.read_text(encoding="utf-8"))


def add_task(database: Path, title: str) -> dict:
    title = title.strip()
    if not title:
        raise ValueError("title must not be empty")
    tasks = load_tasks(database)
    task = {"id": len(tasks) + 1, "title": title, "done": False}
    tasks.append(task)
    database.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    return task


def format_tasks(tasks: list[dict]) -> str:
    if not tasks:
        return "No tasks."
    return "\n".join(
        f"{task['id']}. [{'x' if task['done'] else ' '}] {task['title']}" for task in tasks
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=Path("tasks.json"))
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")
    subparsers.add_parser("list")
    args = parser.parse_args(argv)
    if args.command == "add":
        task = add_task(args.db, args.title)
        print(f"Added task {task['id']}.")
    else:
        print(format_tasks(load_tasks(args.db)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
