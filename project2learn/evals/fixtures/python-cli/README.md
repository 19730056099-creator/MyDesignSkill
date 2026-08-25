# Pocket Tasks

Pocket Tasks is a small command-line task list.

```text
python app.py --db tasks.json add "Read chapter 1"
python app.py --db tasks.json list
```

Tasks persist between invocations. Empty titles are rejected, and listing an empty database prints `No tasks.`.
