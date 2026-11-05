---
name: test-local-chat
description: >-
  Checks that the local Ollama model is resident on the GPU, times a short
  streamed reply with the workspace virtualenv, and smoke-tests
  local_chat/chat.py token streaming. Use when a local model reply is slow,
  or when verifying that the terminal chat client streams from Ollama.
---

# Test local chat

Run from the workspace root that contains `.venv` and `local_chat/chat.py`. Use `.venv/bin/python`. `MODEL` defaults to `dolphin3:8b`. `OLLAMA_HOST` defaults to `http://127.0.0.1:11434`.

## GPU residency

```bash
ollama ps
curl -s http://127.0.0.1:11434/api/ps
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,utilization.memory --format=csv
nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv
```

Pass when `ollama ps` shows the model with processor `100% GPU`, `/api/ps` reports a non-zero `size_vram` for that model, and the compute-apps list includes `/usr/local/lib/ollama/llama-server`.

## Time one streamed reply

```bash
.venv/bin/python - << 'PY'
import os
import time
from ollama import Client

host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
model = os.environ.get("MODEL", "dolphin3:8b")
client = Client(host=host)
t0 = time.perf_counter()
first = None
n = 0
stream = client.chat(
    model=model,
    messages=[{"role": "user", "content": "Reply with one short sentence: what is 2+2?"}],
    stream=True,
    options={"num_predict": 64},
)
for chunk in stream:
    piece = chunk.message.content or ""
    if piece and first is None:
        first = time.perf_counter() - t0
    n += len(piece)
    if chunk.done:
        total = time.perf_counter() - t0
        print(f"first_token_s={first:.2f}")
        print(f"total_s={total:.2f}")
        print(f"chars={n}")
        print(f"eval_count={chunk.eval_count}")
        print(f"eval_duration_s={(chunk.eval_duration or 0)/1e9:.2f}")
        print(f"prompt_eval_count={chunk.prompt_eval_count}")
        print(f"prompt_eval_duration_s={(chunk.prompt_eval_duration or 0)/1e9:.2f}")
        print(f"load_duration_s={(chunk.load_duration or 0)/1e9:.2f}")
        if chunk.eval_count and chunk.eval_duration:
            print(f"tok_per_s={chunk.eval_count / (chunk.eval_duration/1e9):.1f}")
PY
```

Pass when the process exits 0, `first_token_s` is printed, `eval_count` is greater than 0, and `tok_per_s` is printed. `load_duration_s` is weight-load time. Generation time is `eval_duration_s`.

## Smoke-test chat.py

`local_chat/chat.py` is a script. Load it by path.

```bash
.venv/bin/python - << 'PY'
import importlib.util
import os
import time
from ollama import Client

spec = importlib.util.spec_from_file_location("chat", "local_chat/chat.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
model = os.environ.get("MODEL", "dolphin3:8b")
client = Client(host=host)
chat = mod.Chat(client, model)
t0 = time.perf_counter()
first = None
chunks = 0
text = []
for piece in chat.send_message("In two short sentences, name the planet we live on."):
    if first is None:
        first = time.perf_counter() - t0
    chunks += 1
    text.append(piece)
print(f"first_token_s={first:.2f} chunks={chunks} chars={sum(map(len, text))} history={len(chat.messages)}")
print("".join(text))
PY
```

Pass when the process exits 0, `chunks` is greater than 1, `chars` is greater than 0, `history` is 2, and the reply text is non-empty.
