import tempfile
import unittest
from pathlib import Path

from app import add_task, format_tasks, load_tasks


class PocketTasksTests(unittest.TestCase):
    def test_empty_database_lists_no_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "tasks.json"
            self.assertEqual(format_tasks(load_tasks(database)), "No tasks.")

    def test_added_task_persists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "tasks.json"
            add_task(database, "Read chapter 1")
            self.assertEqual(load_tasks(database)[0]["title"], "Read chapter 1")


if __name__ == "__main__":
    unittest.main()
