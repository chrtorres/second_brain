---
name: test-local-harness
description: >-
  Scores the local_harness chat window against live Ollama examples and
  requires acceptance above 95%. Use when changing that window, when a
  browser reply looks wrong, or when checking the live example suite.
---

# Test local harness

Run from `local_harness`, the directory that contains `test_live.py` and `chat_window.py`. `MODEL` defaults to `dolphin3:8b`. `OLLAMA_HOST` defaults to `http://127.0.0.1:11434`.

## Acceptance run

```bash
python3 test_live.py
```

The script starts the window on a free port, checks the page and the chat API, then scores `examples.json` against the live model. Pass when the process exits 0 and the printed `acceptance` is greater than 95%.

## Open the window

```bash
python3 chat_window.py
```

Open `http://127.0.0.1:8765`. Pass a manual check when a sent message appears as a user bubble, the assistant reply streams into the thread, a follow-up can use that reply, Stop ends generation, and New chat clears the thread.
