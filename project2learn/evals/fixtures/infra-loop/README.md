# Line KV Server

Line KV Server accepts TCP connections on port 4040. Commands are one line each:

```text
SET name Alice
GET name
```

It responds with `OK`, `VALUE <value>`, `NOT_FOUND`, or `ERROR <message>`. Multiple clients may connect at the same time.
