from pathlib import Path

project = "Open Source Software Development for Astronomy"

extensions = [
    "myst_parser",  # markdown support
    "sphinx_revealjs",  # build slides.md as reveal.js decks via `-b revealjs`
]

source_suffix = {
    ".md": "markdown",
}

myst_enable_extensions = [
    "attrs_inline",  # lets markdown images/links take a {.class} suffix
]

exclude_patterns = ["_build"]
# Keep empty lecture scaffolds out of the published site until written.
exclude_patterns += [
    path.relative_to(Path(__file__).parent).as_posix()
    for path in Path(__file__).parent.rglob("*.md")
    if not path.read_text(encoding="utf-8").strip()
]

html_theme = "furo"

revealjs_style_theme = "white"
revealjs_static_path = ["_static"]
revealjs_css_files = ["revealjs-custom.css"]
revealjs_script_conf = {
    # true 16:9 instead of reveal.js's 960x700 default - matches modern
    # displays/projectors and removes letterboxing that was shrinking
    # the usable horizontal area.
    "width": 1280,
    "height": 720,
    # top-align content instead of vertically centering it, so a slide
    # with more content grows downward predictably rather than being
    # centered (and thus clipped equally top and bottom).
    "center": False,
}
