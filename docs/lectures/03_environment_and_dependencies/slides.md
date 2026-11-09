---
orphan: true
---

# Environment and dependency management with uv

Prashin Jethwa
09/11/26

## Reproducible scientific computing

You've written a Python analysis. Another researcher wants to run it on their
computer — perhaps years later.

**What do they need besides your code?**

- A suitable Python version
- The required packages, in compatible versions

Together, the Python version and installed packages form the software environment.

## Python environments

An **environment** is a Python interpreter and its installed packages.

- Different projects may require different package versions.
- An **isolated environment** keeps one project's packages separate from others.
- Python's built-in `venv` module creates virtual environments.

## What does a package manager do?

A **package manager** is a tool for installing and managing software packages,
e.g. `pip` for Python.

They handle the following tasks:
- **Dependency identification:** read declared requirements and package metadata
  to identify direct and transitive dependencies — not inspect your source code
- **Dependency resolution:** find mutually compatible versions
- **Downloading and caching:** fetch packages and store them for reuse
- **Installation:** install the resolved packages into an environment

## Direct and transitive dependencies

```text
Your analysis ──→ SciPy ──→ NumPy
```

- Your analysis needs SciPy: a **direct dependency**.
- SciPy needs NumPy: a **transitive dependency** of your analysis.
- `pip install scipy` installs both, selecting compatible versions.

If your analysis also directly imports NumPy, NumPy is a direct dependency too.

## Dependency resolution: finding a solution

```text
A v1 ── requires C < 2
A v2 ── requires C >= 2

B    ── requires C < 2
```

- This is a **constraint-satisfaction problem**.
- Suppose the resolver first tries A v2: its requirement conflicts with B.
- It **backtracks** and selects A v1 instead; both now allow C < 2.
- If no compatible combination exists, resolution fails.

## `uv` is an exceptionally fast Python package manager

```{image} figs/package-manager-benchmarks.png
:alt: Lockfile generation: uv 0.5 s, Pixi 19.5 s, Poetry 30.5 s. Warm-cache installation: uv 2.1 s, Pixi 21.8 s, Poetry 86.6 s, Mamba 104.8 s, pip 163.5 s, Conda 163.6 s.
:width: 1150px
:align: center
```

Lockfile generation is a resolution proxy, not a resolver-only measurement.
Warm-cache installs recreate the environment between runs. Seconds; lower is better.
[OpenTeams, April 2026](https://openteams.com/engineering-blog/benchmark-python-package-managers/):
~25 direct dependencies; median of two runs on Rocky Linux, x86_64.
Results depend on workload and hardware; package builds differ across ecosystems.

Also explore the [Python Package Manager Shootout](https://lincolnloop.github.io/python-package-manager-shootout/).

## From package management to project management

A package manager helps you install and use software. But what happens when you're developing your own project?

- Declare your project's dependencies.
- Isolate your project from other projects.
- Execute your code in the correct environment.
- Reproduce that environment on another computer.

`uv` goes beyond package management: it provides a unified interface for managing and running an entire Python project.

## Scope of Python management tools

| Tool | Package management | Environment management | Project management |
|------|:------------------:|:----------------------:|:------------------:|
| `pip` | ✓ | — | — |
| `venv` | — | ✓ | — |
| `conda` | ✓ | ✓ | ◐ |
| `Poetry` | ✓ | ✓ | ✓ |
| **`uv`** | **✓** | **✓** | **✓** |

*✓ = supported · ◐ = partial support · — = not supported*

**Project management:** Declaring and locking dependencies, maintaining project configuration, and running commands in the project environment.

*[Conda environments](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html) · [Poetry](https://python-poetry.org/docs/)*

## Live Demo

Instructions to reproduce can be found [here](https://prashjet.github.io/oss4astro-course/lectures/03_environment_and_dependencies/walkthrough.html).

## Does developing with `uv` mean everyone must use `uv`?

**No.** In the second part of the demo, we started a **new installable library** from the original Git commit.

- `uv init --lib` generated an importable `src/sequence/` package.
- The generated `[build-system]` selects `uv_build` as a standard build backend; no Hatchling substitution is needed.
- From a clone, users can run `pip install .` in their own environment,
  independently of uv; runtime dependencies are installed too.
- `pip` resolves requirements independently; it does not use `uv.lock` or install
  the development group by default.
- Installing from source and publishing to PyPI are separate steps.

**For a new final project, start with `uv init --lib my-project`.**
We started again from the original commit on a fresh branch.

## Runtime and development dependencies

- **Runtime dependencies** are needed by the program itself (e.g. NumPy).
- **Development dependencies** support work on the project (e.g. Sphinx for documentation).
- `uv add --dev sphinx` records Sphinx in the `dev` dependency group.
- `uv run` and `uv sync` include the `dev` group by default; `--no-dev` excludes it.

**Next lecture:** using Sphinx to build documentation.

## What exactly is `uv.lock`?

`pyproject.toml` declares **requirements**; `uv.lock` records **a resolution**.

| `pyproject.toml` | `uv.lock` |
|---|---|
| Direct dependencies | Direct and transitive dependencies |
| Allowed version ranges | Exact resolved versions |
| Python compatibility requirements | Python/platform-specific alternatives |
| Human-maintained | Automatically generated |

- `uv.lock` is a **universal lockfile**: it can resolve for multiple Python versions and operating systems.
- The same package can appear at different versions, with conditions specifying where each applies.
- A single version may also have multiple platform-specific wheels.
- `uv sync` installs the appropriate locked distributions for the current environment.
- Commit `uv.lock` to Git for reproducible development.

**A lockfile is not simply a list of what's installed on your computer.**

## Semantic versioning: what do version numbers mean?

A common convention is **Semantic Versioning (SemVer)**:

**MAJOR.MINOR.PATCH** — for example, `2.4.1`

- **MAJOR** (`2 → 3`): incompatible API changes.
- **MINOR** (`2.4 → 2.5`): backward-compatible new functionality.
- **PATCH** (`2.4.1 → 2.4.2`): backward-compatible bug fixes.

For **stable releases (1.0.0 onward)**, later versions within the same major series should preserve compatibility under SemVer. Before 1.0.0, the public API may change freely.

But:
- Not all Python packages follow SemVer.
- Version numbers are conventions and promises, not guarantees of compatibility.
- Dependency resolvers do not automatically enforce SemVer rules.

**SemVer communicates compatibility expectations; it does not define dependency constraints.**

## PEP 440: specifying compatible versions

Python uses **PEP 440** to define version ordering and dependency version specifiers.

| Requirement | Permitted stable versions |
|---|---|
| `numpy>=2.0` | 2.0 and newer, including 3.x |
| `numpy>=2.0,<3` | 2.x |
| `numpy==2.2.0` | Exactly 2.2.0 |
| `numpy~=2.2` | >=2.2, <3.0 |
| `numpy~=2.2.0` | >=2.2.0, <2.3.0 |

- `>=2.0` does **not** imply `<3`, even if a package follows SemVer.
- Package authors explicitly declare the version ranges they support.
- Resolvers combine constraints from direct and transitive dependencies.

Example: A requires `numpy>=2.0`, B requires `numpy<2.2`; a compatible solution lies in `>=2.0,<2.2`.

**SemVer helps authors decide which versions are compatible. PEP 440 tells the resolver which versions are allowed.**

## From package management to reproducible projects

| Requirement | `uv` provides |
|---|---|
| **Declare** | `uv add` / `uv remove` — manage dependencies in `pyproject.toml` |
| **Isolate** | `.venv` — separate project environment |
| **Execute** | `uv run` — synchronize the environment and execute code |
| **Reproduce** | `uv.lock` and `uv sync` — recreate resolved dependencies |
| **Package / Distribute** | `src/` and `[build-system]` — create an installable package |

**The environment is disposable; the project specification and lockfile are what we preserve and share.**

`uv` integrates development and package installation; standard build metadata keeps the package usable with other installers.

## New project requirements: environments & dependencies

Your project should now:

- Be an **installable Python package**, with `[build-system]` in `pyproject.toml`.
- Install from a fresh clone with `pip install .`, independently of uv.
- Declare runtime dependencies separately from development dependencies.
- Commit a development lockfile; keep `.venv` out of Git.
- Document installation and execution in the README.

Recommended: `uv init --lib` for new projects; equivalent workflows are welcome.

See [Project Requirements](https://github.com/prashjet/oss4astro-course/blob/main/project_requirement.md) for the full list.
