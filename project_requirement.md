
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

## Python environments, dependencies & packaging

- structure your project as an installable Python package,
  - `uv init --lib` is the recommended starting point for a new project; equivalent tooling is welcome,
- include standard build-system metadata (`[build-system]`) in `pyproject.toml`,
- ensure a fresh clone can be installed with `pip install .`, independently of uv,
- use `uv` (or an equivalent tool) to manage your project's Python environment and dependencies,
- declare runtime dependencies in `pyproject.toml`,
  - distinguish them from development dependencies (e.g. documentation and testing tools),
- commit a lockfile (`uv.lock` or equivalent) for reproducible development,
- do not commit your virtual environment (`.venv`) to Git,
- document installation and execution in the README,
  - a colleague should be able to install the package from a fresh clone and run your code using these instructions.
