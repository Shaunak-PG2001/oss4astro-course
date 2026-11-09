---
orphan: true
---

# Demo: uv — cue sheet

## Starting point

- Repo: [prashjet/sequence](https://github.com/prashjet/sequence); commit [`4195620`](https://github.com/prashjet/sequence/commit/419562011e7d658347e87b99ebaf9816e489a029).
- Before class: `uv --version`; open checkout in VS Code.
- Fresh clone: `git clone https://github.com/prashjet/sequence.git`; `cd sequence`.
- Branch: `git switch -c lecture-03 4195620`.

## Initialize / select Python

- `uv init`
- Inspect `pyproject.toml`, `.python-version`, starter `main.py`.
- **Supported versions** (`requires-python`) ≠ **local interpreter** (`.python-version`).
- `uv python pin 3.12` — inspect changed pin; requirements unchanged.
- Pin must satisfy `requires-python`; adjust minimum only if code supports it.
- uv can download Python if needed.

## Declare / inspect

- `uv add numpy` — watch resolution, `.venv` creation, installation.
- `pyproject.toml`: declared requirements / allowed versions.
- `uv.lock`: resolved choices across supported Python versions/platforms; don't edit.
- Multiple NumPy versions may be locked; only the appropriate one is installed.

## Isolate

- Expand `.venv` in VS Code.
- `uv run python -c "import sys; print(sys.executable)"`
- `uv run python -c "import numpy; print(numpy.__version__)"`
- Compare installed version with lockfile; no manual activation.
- `git check-ignore .venv` — keep environment out of Git.

## Execute

- Replace `main.py`:

```python
import numpy as np


def even(n):
    return 2 * np.arange(n)


print(even(10))
```

- `uv run python main.py` — ten even numbers: 0, 2, …, 18.

## Add / remove dependencies

- `uv tree`
- `uv add matplotlib`; `uv tree` — inspect project files and transitive packages.
- NumPy remains direct, even though Matplotlib also requires it.
- `uv remove matplotlib`; `uv tree` — unused transitive packages disappear.

## Reproduce

- Delete **only this checkout's `.venv`** in VS Code; keep project files.
- `uv run python main.py` — recreates environment, installs, runs.
- `uv sync` — synchronize without running code.
- `uv sync --locked` — fail if lockfile needs updating.
- Cached packages explain speed; dependency reproduction ≠ identical numerical results.

## Share / finish

- README: install uv, then `uv run python main.py`.
- Commit: code, README, `.gitignore`, `pyproject.toml`, `uv.lock`, `.python-version`.
- Ignore: `.venv`, caches, generated outputs.
- `git status`; `git diff`; commit, push branch, open PR.
- Recap: **declare → isolate → execute → reproduce**.
- Return to semantic-versioning slide.
