---
name: comment-confusing-code
description: >-
  Adds comments that explain confusing or indirect code without changing
  behavior, then checks that the Python files still parse. Use when the
  user asks to comment confusing or indirect code in named files.
---

# Comment confusing code

Read each named file. Add a comment only where the code is confusing or indirect. Put it on the line above that code and state why it is written that way. Do not restate the next line. Do not change behavior. Leave clear code uncommented.

## Check

From the directory that contains the edited Python files, set `<files>` to those paths. In the second command, `<files>` is a tuple of quoted paths, such as `'a.py', 'b.py'`.

```bash
python3 -m py_compile <files> && python3 -c "
import ast
for name in (<files>):
    ast.parse(open(name).read())
print('ok')
"
```

Pass when the command exits 0 and prints `ok`.
