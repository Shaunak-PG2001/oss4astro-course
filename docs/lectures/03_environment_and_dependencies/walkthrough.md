---
orphan: true
---

# Walkthrough: Environment and dependency management

This walkthrough reproduces the live demonstration using the [sequence example repository](https://github.com/prashjet/sequence). You can also adapt the commands to your own Python project by substituting your own scripts and dependencies.

## Install uv

Follow the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/) for your operating system.

## Initialize the project

For the demo's exact starting point, clone the example and create a branch:

```sh
git clone https://github.com/prashjet/sequence.git
cd sequence
git switch -c lecture-03 4195620
```

If your project directory already exists, enter it and run:

```sh
uv init
```

Or create a new project directory:

```sh
uv init my-project
cd my-project
```

Useful initialization options:

- `uv init --python 3.12`: select Python 3.12 at initialization.
- `uv init --bare`: create minimal project metadata without starter files.
- `uv init`: explicitly initialize a non-packaged application; used in the first part of this walkthrough.
- `uv init --name my-package`: choose a name independent of the directory.

Options can be combined, e.g. `uv init --python 3.12 my-project`. Use `uv init --help` for more.

Inspect the files from `uv init`:

- **`pyproject.toml`**: project metadata, supported Python versions, direct dependencies.
- **`.python-version`**: interpreter selection for local development.
- **`main.py`**: starter script; replace it with your own code.

If a project already has a `pyproject.toml`, inspect it rather than reinitializing it.

## Select a Python version

`requires-python` in `pyproject.toml` declares the Python versions your project supports; `.python-version` selects your local interpreter. Their initial values depend on the Python version available when the project is initialized.

```sh
uv python pin 3.12
```

Inspect `.python-version` again. Pinning does **not** change `requires-python`, and the selected Python must satisfy it. Don't lower `requires-python` unless your code and dependencies actually support older versions. uv can download a suitable Python interpreter if needed.

## Declare dependencies

```sh
uv add numpy
```

Observe resolution and installation, then inspect:

- **`pyproject.toml`**: NumPy is a direct dependency, with an allowed version range.
- **`uv.lock`**: exact resolved versions, dependency relationships and available distributions.
- **`.venv`**: the particular environment installed on this computer.

`uv.lock` is a **universal lockfile**: it can record different resolutions for different supported Python versions and platforms. It may list multiple NumPy versions, and each version may also list multiple platform-specific wheels. The current environment installs only the applicable choice. Don't edit the lockfile by hand.

## Inspect the isolated environment

Open `.venv` in your editor or file browser. Check the interpreter and NumPy version:

```sh
uv run python -c "import sys; print(sys.executable)"
uv run python -c "import numpy; print(numpy.__version__)"
```

`uv run` uses the project environment without manual activation and synchronizes it automatically when needed. Other projects can use different Python and package versions.

If using Git, check that the environment is ignored:

```sh
git check-ignore .venv
```

If necessary, add `.venv/` to `.gitignore`.

## Execute code

In the demo, replace the starter `main.py` with:

```python
import numpy as np


def even(n):
    return 2 * np.arange(n)


print(even(10))
```

**Run project code with `uv run`:**

```sh
uv run python main.py
```

**This is the normal way to execute Python code in a uv-managed project.** Before running the command, `uv` checks that the project's environment is synchronized with its requirements and lockfile, updates it if needed, and uses the project's Python interpreter. You don't have to activate `.venv` or run `uv sync` first.

Expected output:

```text
[ 0  2  4  6  8 10 12 14 16 18]
```

For your own project, replace `main.py` with your script. Use the same `uv run ...` pattern for other commands that need the project's environment.

## Add and remove dependencies

Compare the dependency tree before and after adding Matplotlib:

```sh
uv tree
uv add matplotlib
uv tree
```

Matplotlib is now a **direct dependency**, while packages it requires are **transitive dependencies**. NumPy remains direct because we explicitly declared it, even though Matplotlib also requires it. Declare packages your own code imports, even if another dependency happens to require them.

Remove Matplotlib again:

```sh
uv remove matplotlib
uv tree
```

uv updates the requirements, lockfile and environment. Packages no longer required by anything are removed; NumPy remains. In the demo we do not write plotting code.

## Recreate the environment

Keep `pyproject.toml` and `uv.lock`, but delete **only this project's `.venv` directory** using your editor or file browser. Then run:

```sh
uv run python main.py
```

`uv run` automatically recreates and synchronizes the environment **before** running the script. You do not need a separate `uv sync` first.

To synchronize without executing code:

```sh
uv sync
```

To require an up-to-date lockfile instead of allowing uv to update it:

```sh
uv sync --locked
```

Cached packages make recreation fast; this is not a cold-cache download benchmark. Reproducing dependencies also does not guarantee identical numerical results across hardware and operating systems.

## Start again: create an installable library

We have demonstrated how to reproduce an **application**. Now we will initialize a **new, installable library**, rather than restructure the first project. We will start from the **same original Git commit** on a fresh branch of the existing GitHub repository.

### Start from a fresh branch

From the `sequence/` checkout used in the first part, save the uncommitted demo files and start again from the original commit:

```sh
git stash push -u -m "lecture-03 application demo"
git switch -c lecture-03-library 4195620
uv init --lib
```

The stash preserves the first demo's uncommitted changes. The new branch starts at the original commit; `uv init --lib` initializes the library in this checkout.

### What's new with `--lib`?

Inspect the generated files. A typical layout is:

```text
sequence/
├── pyproject.toml
├── README.md
├── .python-version
└── src/
    └── sequence/
        └── __init__.py
```

Unlike the first application initialization, `--lib` explicitly creates an **importable package** under `src/` and a **`[build-system]` section** in `pyproject.toml`. A standalone `main.py` is not needed. The `src/` layout keeps importable code separate from repository-level scripts and configuration.

Inspect the `[build-system]` section that your version of uv generated. For example:

```toml
[build-system]
requires = ["uv_build>=0.11.25,<0.12.0"]
build-backend = "uv_build"
```

The exact `uv_build` version range may differ. **Keep the generated configuration; do not replace it with Hatchling.** A build backend creates installable distributions from your source. `requires` here lists **build-time tools**, not dependencies required when someone runs your library. The configuration follows standard Python packaging conventions, so tools such as pip can use it without the user installing the uv command.

### Add the library's runtime dependency and code

```sh
uv add numpy
```

Inspect `pyproject.toml`: NumPy is now a runtime dependency under `[project]`, and `uv.lock` records a resolution. Replace `src/sequence/__init__.py` with:

```python
import numpy as np


def even(n):
    return 2 * np.arange(n)
```

Synchronize and import the installed library:

```sh
uv sync
uv run python -c "from sequence import even; print(even(10))"
```

Expected output:

```text
[ 0  2  4  6  8 10 12 14 16 18]
```

For a packaged library, `uv sync` installs the project itself in **editable mode** into `.venv`, alongside its dependencies. Editing the package's Python files does not normally require reinstalling it. The import succeeds because the project is installed, not merely because the source directory happens to be the current working directory.

### Installation without uv

Having created an **importable package**, another user can clone the repository and, in their own Python environment, run:

```sh
python -m pip install .
python -c "from sequence import even; print(even(10))"
```

`pip` uses the project's standard build metadata and resolves its runtime dependencies independently. It does **not** read `uv.lock` or install the development dependency group.

## Add a development dependency: Sphinx

NumPy is a **runtime dependency**: the installed package needs it to run. Other packages are tools we need only while **developing** the project.

Next week's lecture introduces Sphinx, which generates project documentation. Add it as a development dependency:

```sh
uv add --dev sphinx
```

Inspect `pyproject.toml`:

- NumPy is listed under `[project]` → `dependencies`.
- Sphinx is listed under `[dependency-groups]` → `dev`.
- `uv.lock` records Sphinx and its transitive dependencies too.

```sh
uv tree
```

By default, `uv sync` and `uv run` include the development dependency group. To exclude it, use `uv sync --no-dev` (you don't need to run this during the demo).

**Key point:** `[dependency-groups]` records development requirements separately from the package's runtime dependencies. A normal `pip install .` does not install the dev group. We'll actually configure and use Sphinx next week.

## Share the project

Commit the `src/` package, `pyproject.toml`, `uv.lock`, `.python-version` and README instructions. Ignore `.venv`, caches and generated outputs.

A README might say:

```markdown
## Installation and use

From a clone, in your own Python environment:

    pip install .
    python -c "from sequence import even; print(even(10))"

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

    uv run python -c "from sequence import even; print(even(10))"
```

Users can install the package with pip; developers can recreate the locked
environment with uv. Review and commit on the demo branch:

```sh
git status
git diff
git add -A
git diff --cached
git commit -m "Initialize installable sequence library"
```

Optionally share the branch and open a pull request:

```sh
git push -u origin lecture-03-library
```

## Additional uv features (for reference)

These commands are **not part of the live demo**:

- `uvx ruff check main.py` — run a tool in an isolated environment without adding it to the project.
- `uv run --no-project --with numpy python my_script.py` — run a standalone script with a temporary dependency.
- `uv lock --upgrade` — re-resolve dependencies, allowing newer compatible versions.
- `uv lock --upgrade-package numpy` — request an upgrade of one locked dependency.
- `uv run --no-sync python main.py` — skip automatic environment synchronization.
- `uv sync --frozen` — use the existing lockfile without checking whether it matches the project requirements.

See the [uv project guide](https://docs.astral.sh/uv/guides/projects/) for more.

## Recap: managing a reproducible Python project

| Requirement | Tool or file | Purpose |
|---|---|---|
| **Declare** | `uv add` / `uv remove`, `pyproject.toml` | Manage declared dependencies |
| **Isolate** | `.venv` | Keep packages separate from other projects |
| **Execute** | `uv run` | Synchronize the environment and run code |
| **Reproduce** | `uv.lock`, `uv sync` | Recreate resolved dependencies |
| **Package / Distribute** | `src/`, `[build-system]` | Make code installable with standard tools; publishing comes later |

Three files play different roles:

- **`pyproject.toml`** specifies requirements and compatibility ranges.
- **`uv.lock`** records resolved versions, potentially conditional on Python/platform.
- **`.venv`** contains the packages installed locally.

**The environment is disposable; the project specification and lockfile are what we preserve and share.**
