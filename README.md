# Open Source Software Development for Astronomy

This repository contains resources for the course Open Source Software Development for Astronomy, held at the University of Vienna during:
- [winter semester 2026](https://ufind.univie.ac.at/en/course.html?lv=450102&semester=2026W),
- [winter semester 2023](https://ufind.univie.ac.at/en/course.html?lv=450102&semester=2023W)

The aim of this course (inspired by the [Code/Astro](https://semaphorep.github.io/codeastro/) workshops) is to enable MSc/PhD students in astronomy to develop open source software packages for research.

## Lecture notes 

| Date | Lecture | Slides | Demo Notes |
|---|---|---|---|
| 05/10 | Motivation | [link](https://prashjet.github.io/oss4astro-course/present/lectures/01_motivation/slides.html) | n/a |
| 12/10 | Discuss Project Ideas | n/a | n/a |
| 19/10 | Version control and collaboration | [link](https://prashjet.github.io/oss4astro-course/present/lectures/02_intro_to_git/slides.html) | [link](https://prashjet.github.io/oss4astro-course/lectures/02_intro_to_git/walkthrough.html) |
| 09/11 | Environment and dependency management | ... | ... |
| 16/11 | Documentation | ... | ... |
| 23/11 | Testing | ... | ... |
| 30/11 | Code quality: linting, formatting, and type hints | ... | ... |
| 07/12 | Continuous integration | ... | ... |
| 14/12 | Packaging: project structure and namespacing | ... | ... |
| 04/01 | Publishing and citing a release | ... | ... |
| 11/01 | Community building: contribution guidelines, codes of conduct, and welcoming new contributors | ... | ... |

[Project requirements and assessment checklist](project_requirement.md)

## Student Software Packages

A list of student software packages completed during this course:

### 2026

| Student                   | Repository    |
| --------                  | -------       |
| ...                       | ...           |

### 2023

| Student                   | Repository                   |
| --------                  | -------                   |
| Marco Janach & Simon Benke| [CelestialCanvas](https://github.com/SimonPBe/CelestialCanvas)    |
| Jonathan Flunger          | [gammaforge](https://github.com/jonathanflunger/gammaforge)    |
| Magdalena Forusova        | [H5CosmoKit](https://github.com/forusovam46/H5CosmoKit)    |
| David Hernandez           | [standard classification](https://github.com/Starvexx/standard_classification)    |
| Katharina Kain            | [DOGcosmoS](https://github.com/katharinaka/DOGcosmoS.git)    |
| Tano Kender               | [Isopod](https://github.com/InkAtom/Isopod)    |
| Dominik Loidolt           | [cmp_tool](https://github.com/blue-bit-shift/cmp_tool)   |
| Lukas Orion & Jim Buisman | [NOrbit](https://github.com/Lukas-Orion/NOrbit)   |
| Luise Pevestorff          | [IMAGINE](https://github.com/luisepevestorff/IMAGINE)   |
| Laura Posch               | [StarTracer](https://github.com/laurap81/StarTracer)   |
| Alena Rottensteiner       | [IsoModulator](https://github.com/rottenstea/Empirical_isochrones)   |
| Cameren Swiggum           | [dash_gaia_orbits](https://github.com/CSwigg/dash_gaia_orbits)   |
| Josef Thomas Tucek        | [QUEQSolver](https://github.com/josef223/QUEQSolver)   |

## Repository Structure

Resources for each lecture are in `docs/lectures/`. Each lecture has:
- slides,
- a walkthrough with detailed instructions on the demo plus some additional resources, 
- a stripped-back script listing commands used in the demo

## Maintaining the course materials

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run
these commands from the repository root:

```sh
uv sync --locked
uv run --locked sphinx-build -W --keep-going -b html docs docs/_build/html
uv run --locked sphinx-build -W --keep-going -b revealjs docs docs/_build/revealjs
mkdir -p docs/_build/html/present
cp -R docs/_build/revealjs/. docs/_build/html/present/
uv run python -m http.server 8000 --directory docs/_build/html
```

Open <http://localhost:8000> for the notes, or
<http://localhost:8000/present/lectures/02_intro_to_git/slides.html> for a deck.
Stop the server with Ctrl-C. Before repeating the copy command, remove the
generated `docs/_build/html/present/` directory to avoid retaining stale files.

To add a lecture, fill in its files under `docs/lectures/`, mark the populated
pages with the YAML front matter shown below, and update the schedule links above.

```yaml
---
orphan: true
---
```

This marks each page as standalone: students reach it through README links,
without needing a Sphinx toctree entry. Empty Markdown scaffolds are automatically excluded from builds. Keep
`future_changes.md` as an ignored local planning file.

Pull requests check both builds and treat warnings as errors. Merges to `main`
also publish the notes and decks to GitHub Pages.
