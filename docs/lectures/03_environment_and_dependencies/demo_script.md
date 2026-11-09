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

- `uv init` (in the existing Git checkout): initialize the application project.
- Inspect `pyproject.toml`, `.python-version`, starter `main.py`.
- **Supported versions** (`requires-python`) ≠ **local interpreter** (`.python-version`). Don't assume the initial Python version is 3.9; inspect what uv selected.
- `uv python pin 3.12` — inspect changed pin; `requires-python` is unchanged.
- Pin must satisfy `requires-python`. Only claim older-version compatibility if code and dependencies support it.
- uv can download Python if needed.

## Declare / inspect

- `uv add numpy` — watch resolution, `.venv` creation, installation.
- `pyproject.toml`: direct requirement and allowed versions.
- `uv.lock`: exact resolved choices across supported Python versions/platforms; don't edit by hand.
- Multiple NumPy versions **may** be locked; distinguish separate versions from multiple wheels for one version. Only the applicable distribution is installed locally.

## Isolate

- Expand `.venv` in VS Code.
- `uv run python -c "import sys; print(sys.executable)"`
- `uv run python -c "import numpy; print(numpy.__version__)"`
- Compare installed version with lockfile; no manual activation.
- `git check-ignore .venv` — keep environment out of Git.

## Execute

- Replace starter `main.py`:

```python
import numpy as np


def even(n):
    return 2 * np.arange(n)


print(even(10))
```

- `uv run python main.py` — **the normal way to run commands in a uv project**: synchronize dependencies if needed, select the project interpreter, then execute. Ten even numbers: 0, 2, …, 18.

## Add / remove dependencies

- `uv tree` — initial tree with NumPy.
- `uv add matplotlib`; `uv tree` — compare requirements, lockfile, transitive packages.
- NumPy remains a direct dependency, even though Matplotlib also requires it.
- `uv remove matplotlib`; `uv tree` — unused transitive packages disappear.
- **Do not add plotting code**: Matplotlib is only a dependency-graph example.

## Reproduce

- Delete **only this checkout's `.venv`** in VS Code; retain `pyproject.toml` and `uv.lock`.
- `uv run python main.py` — **automatically synchronizes**, recreates environment, then runs.
- `uv sync` — synchronize explicitly, without running code.
- `uv sync --locked` — fail if the lockfile needs updating.
- Cached packages explain speed; dependency reproduction ≠ identical numerical results across hardware.

## Package: start again as an installable library

- Let's start again from a fresh branch at the original commit, this time initializing a library.
- Save the uncommitted application-demo changes before switching branches:

```sh
git stash push -u -m "lecture-03 application demo"
git switch -c lecture-03-library 4195620
uv init --lib
```

- Inspect the generated `pyproject.toml`, `.python-version`, `README.md`, and `src/sequence/__init__.py` (exact starter files may vary by uv version).
- **What is new with `--lib`?** Unlike the first `uv init`, this explicitly creates a library: `src/sequence/` holds importable code, `[build-system]` configures a build backend, and the project itself is installable. There is no standalone `main.py`.
- Inspect the actual generated `[build-system]`. Current uv uses `uv_build`, e.g.:

```toml
[build-system]
requires = ["uv_build>=0.11.25,<0.12.0"]
build-backend = "uv_build"
```

- **Do not overwrite** the generated version constraint or replace `uv_build` with Hatchling. `uv_build` is a standard PEP 517 build backend, distinct from the `uv` CLI. `requires` here means **build** dependencies, not runtime dependencies.
- `uv add numpy` — inspect NumPy under `[project].dependencies` and changes to `uv.lock`.
- Replace `src/sequence/__init__.py` with:

```python
import numpy as np


def even(n):
    return 2 * np.arange(n)
```

- `uv sync` — installs the project in editable mode, along with NumPy.
- `uv run python -c "from sequence import even; print(even(10))"` — expected output: `[ 0  2  4  6  8 10 12 14 16 18]`.
- **Portable installation:** in a separate environment, another user can run `pip install .` from a clone. `pip` uses `[build-system]` and installs runtime requirements, but does **not** use `uv.lock` or install dev dependencies.
- Installable from source ≠ published on PyPI; publishing comes later.

## Development dependencies / bridge to next lecture

- Runtime: NumPy; development: Sphinx for next week's documentation.
- `uv add --dev sphinx`; inspect `[dependency-groups]` → `dev`.
- `uv tree` — Sphinx's transitive dependencies.
- `uv run` / `uv sync` include `dev` by default; `--no-dev` excludes it.
- Package users don't need Sphinx; **no Sphinx setup/build today**.

## Share / finish

- README: `pip install .` in a user's own environment; import `even`.
  Development: install uv, then `uv run python -c "from sequence import even; print(even(10))"`.
- Commit code, README, `.gitignore`, `pyproject.toml`, `uv.lock`, `.python-version`.
- Ignore `.venv`, caches, build outputs.
- `git status`; `git diff`.
- `git add -A` — inspect staged changes; ensure `.venv` is ignored.
- `git commit -m "Initialize installable sequence library"`
- Optional: `git push -u origin lecture-03-library`; open PR.
- **Return to slides at “Does developing with uv mean everyone must use uv?”**
