---
orphan: true
---

# Walkthrough: Environment and dependency management

Follow the demo's uv commands in your own project. The examples use NumPy and
Matplotlib; substitute the dependencies your project needs.

## Install uv

Follow the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/)
for your operating system.

## Initialize the project

If your project directory already exists, enter it and run:

```sh
uv init
```

If you haven't created a directory yet, uv can create it for you:

```sh
uv init my-project
cd my-project
```

Some useful initialization options:

- `uv init --python 3.12`: choose Python 3.12 at initialization.
- `uv init --bare`: create only `pyproject.toml`, without starter files.
- `uv init --lib`: create a library project with a package structure; we'll
  discuss packaging later in the course.
- `uv init --name my-package`: set the project name independently of the directory name.

Options can also be combined with a new directory, e.g.
`uv init --python 3.12 my-project`. Use `uv init --help` for the full list.

For the plain `uv init` used in the demo, inspect the generated files:

- **`pyproject.toml`**: project metadata, supported Python versions, and dependencies.
- **`.python-version`**: the Python version selected for local development.
- **`main.py`**: a starter script you can run or replace with your own code.

If the project already has a `pyproject.toml`, inspect its configuration rather
than initializing it again.

## Select a Python version

Compare `requires-python` in `pyproject.toml` with `.python-version`.
The first declares the versions your project supports; the second selects the
interpreter used locally.

```sh
uv python pin 3.12
```

Inspect `.python-version` again. Pinning does not change `requires-python`:
Python 3.12 must satisfy that requirement. If initialization selected a newer
minimum, only lower it if your code and dependencies support the older Python.
uv can download a suitable interpreter if needed.

## Declare dependencies

```sh
uv add numpy
```

Observe the resolution and installation output, then inspect:

- **`pyproject.toml`**: NumPy is a direct dependency, with an allowed version range.
- **`uv.lock`**: resolved versions and package distributions, maintained by uv.
- **`.venv`**: the environment installed for this project on this computer.

The lockfile can contain alternative versions for different supported Python
versions or platforms. Your local environment installs the appropriate choices;
`uv.lock` is not simply a list of what is installed locally. Don't edit it manually.

## Inspect the isolated environment

Open `.venv` in your editor or file browser. Check the interpreter and NumPy version:

```sh
uv run python -c "import sys; print(sys.executable)"
uv run python -c "import numpy; print(numpy.__version__)"
```

Compare the installed version with the lockfile. `uv run` uses the project
environment without manual activation. Other projects can use different versions.

If using Git, check that the generated environment is ignored:

```sh
git check-ignore .venv
```

If it isn't ignored, add `.venv/` to `.gitignore`.

## Execute code

Run the starter script, or substitute the path to your own script:

```sh
uv run python main.py
```

The command runs with the project's interpreter and dependencies.

## Add and remove dependencies

Inspect the dependency tree, then add another package:

```sh
uv tree
uv add matplotlib
uv tree
```

Compare the tree and project files before and after. Matplotlib is a direct
dependency; packages it requires are transitive dependencies. NumPy remains
direct because you explicitly declared it. Declare packages your own code
imports, even if another dependency also requires them.

Remove Matplotlib again:

```sh
uv remove matplotlib
uv tree
```

uv updates the requirements, lockfile, and environment. Transitive packages
that are no longer needed are removed; NumPy remains. Keep Matplotlib installed
if your own code needs it.

## Recreate the environment

Keep `pyproject.toml` and `uv.lock`, but delete **only this project's `.venv`
directory** using your editor or file browser. Then run:

```sh
uv run python main.py
```

uv recreates the environment, installs its dependencies, and runs the script.
The environment is disposable; the project files let you rebuild it.

To synchronize the environment without executing code:

```sh
uv sync
```

To require an up-to-date lockfile instead of allowing uv to update it:

```sh
uv sync --locked
```

Cached packages make recreation fast; this does not measure cold-cache download
speed. Recreating dependencies does not guarantee identical numerical results
across hardware and operating systems.

## Share the project

Commit your code, `pyproject.toml`, `uv.lock`, `.python-version`, and README run
instructions. Ignore `.venv`, caches, and generated outputs.

Document that uv must be installed and show the command needed to run your code,
for example `uv run python main.py`. A colleague can clone the repository and use
that command to recreate the environment and execute the script.

Review your changes with `git status` and `git diff`, commit them on your feature
branch, and open a pull request.

Reference: [uv project guide](https://docs.astral.sh/uv/guides/projects/).
