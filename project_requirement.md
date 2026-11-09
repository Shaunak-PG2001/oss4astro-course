
# Project Requirements

A list of requirements your software package will be graded against, to be
updated as the course progresses.

Any point which is explicitly optional will be marked with a (*). All other
points are required however you are free to choose alternative tools if you 
prefer. In that case, I will ask you to briefly explain your choice of tooling.

Two weeks before the project submission, each item in the list will be allocated
a number of points. For certain points, I will ask you to provide evidence e.g.
a reference to a relevant pull request. These points will contribute 60% of your
final grade, with the final 40% coming from the project presentation.

## git & GitHub

- use Git & GitHub for version control,
- use PR (pull requests) for every new feature, bug fix etc
  - do not merge directly to main!
  - keep individual PRs *well-scoped* i.e. as small as possible to implement a single useful modification...
- collaborate at least once via GitHub issues & PRs:
  - pick a partner in the class,
  - raise an issue in your repository describing some change you would like to make (keep it simple!)
  - invite a colleague from this class to address the issue,
  - to do this: fork your partner's repo, make the change, raise a PR

## Python environments and dependencies

Your project must be structured as an **installable Python package**, with its environment and dependencies managed reproducibly.

Requirements:

- **Package structure:** Organize your code as an installable Python package, with appropriate `[build-system]` configuration in `pyproject.toml`.
- **Installation:** The package must be installable from a fresh clone using `pip install .`, without requiring `uv`.
- **Dependencies:** Declare runtime dependencies in `pyproject.toml`, distinguishing them from development dependencies (such as testing and documentation tools).
- **Reproducibility:** Include a lockfile (`uv.lock` or equivalent) in the Git repository.
- **Environment isolation:** Use an isolated Python environment for development. Do not commit `.venv/` or other generated environments.
- **Documentation:** Provide README instructions explaining how to install and use the package, and how to recreate the development environment.

We recommend using [`uv`](https://docs.astral.sh/uv/) for dependency and environment management. For a new project, `uv init --lib` provides a suitable starting structure.

Equivalent tools and workflows are acceptable, provided they satisfy the requirements above.

**Verification:** Another student should be able to clone your repository, install your package in a fresh Python environment, and import and use its functionality by following your README.
