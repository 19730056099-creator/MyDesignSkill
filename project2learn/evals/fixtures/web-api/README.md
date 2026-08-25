# Tiny Items API

The service exposes:

- `GET /items` — return all items.
- `POST /items` with `{"name":"Notebook"}` — create an item.
- Other paths return 404; invalid JSON or a blank name returns 400.

Run with `node server.js`, then send requests to port 3000.
