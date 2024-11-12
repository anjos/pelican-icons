# SPDX-FileCopyrightText: Copyright © 2024 André Anjos <andre.dos.anjos@gmail.com>
# SPDX-License-Identifier: MIT

import logging
import pathlib

from bs4 import BeautifulSoup
import pytest


def _assert_log_contains(
    records: list[logging.LogRecord], message: str, level: int, count: int = 1
) -> None:
    """Assert that the log records contains the given count of matching
    messages.

    Parameters
    ----------
    records
        All logging records collected.
    message
        The message that must be searched for.
    level
        The level of the message that must match.
    count
        The number of times the message must appear.
    """

    filtered = [k for k in records if k.levelno == level and message in k.message]

    assert len(filtered) == count, (
        f"Found {len(filtered)} records containing `{message}` at "
        f"level {level} ({logging.getLevelName(level)}) instead "
        f"of {count} (expected)."
    )


def _assert_log_no_errors(
    records: list[logging.LogRecord], level: int = logging.ERROR
) -> None:
    """Assert that the log records do not contain any message with a level
    equal or above the indicated value.

    Parameters
    ----------
    records
        All logging records collected.
    level
        The level of the message that must match.
    """

    filtered = [k for k in records if k.levelno >= level]

    assert len(filtered) == 0, (
        f"Found {len(filtered)} record(s) containing level {level} "
        f"({logging.getLevelName(level)}) at least."
    )


@pytest.mark.parametrize("subdir", ["basic-usage"])
def test_basic_usage(setup_pelican: tuple[list[logging.LogRecord], pathlib.Path]):
    records, pelican_output = setup_pelican

    def _check_article(path: pathlib.Path):
        assert path.exists()

        with path.open() as f:
            soup = BeautifulSoup(f, "html.parser")

        link = soup.find_all("link")
        num_stylesheets = 3
        assert len(link) == num_stylesheets
        assert link[0].attrs["href"].endswith("fontawesome.min.css")
        assert link[1].attrs["href"].endswith("solid.min.css")
        assert link[2].attrs["href"].endswith("bootstrap-icons.min.css")

        para = soup.find_all("p")

        assert para[0].text.startswith("Icon embedding example")
        svg = para[0].find_all("svg")
        assert len(svg) == 1

        assert svg[0].attrs["fill"] == "currentColor"
        assert svg[0].attrs["width"] == "1em"
        assert svg[0].attrs["height"] == "1em"

        assert para[1].text.startswith("Icon embedding styling")
        svg = para[1].find_all("svg")
        assert len(svg) == 1

        assert svg[0].attrs["fill"] == "green"
        assert svg[0].attrs["width"] == "3em"
        assert svg[0].attrs["height"] == "3em"

        assert para[2].text.startswith("Icon font-awesome example:")
        icon = para[2].find_all("i")
        assert len(icon) == 1
        assert icon[0].text == ""
        assert icon[0].attrs["class"] == ["fas", "fa-circle-check"]

        assert para[3].text.startswith("Icon bootstrap icons example:")
        icon = para[3].find_all("i")
        assert len(icon) == 1
        assert icon[0].text == ""
        assert icon[0].attrs["class"] == ["bi", "bi-check-circle"]

        assert para[4].text.startswith("Icon styling example:")
        span = para[4].find_all("span")
        assert len(span) == 1
        assert span[0].attrs["style"] == "color: red; font-size: 3em;"
        icon = span[0].find_all("i")
        assert len(icon) == 1
        assert icon[0].text == ""
        assert icon[0].attrs["class"] == ["bi", "bi-check-circle"]

    _check_article(pelican_output / "article-rst.html")
    _check_article(pelican_output / "article-markdown.html")

    _assert_log_no_errors(records)
    _assert_log_contains(
        records,
        message="Loading contents of file `circle-check.svg`",
        level=logging.INFO,
        count=1,
    )


@pytest.mark.parametrize("subdir", ["gracious-error"])
def test_gracious_error(setup_pelican: tuple[list[logging.LogRecord], pathlib.Path]):
    records, pelican_output = setup_pelican

    def _check_article(path: pathlib.Path):
        assert path.exists()

        with path.open() as f:
            soup = BeautifulSoup(f, "html.parser")

        # there should be no stylesheets linked
        link = soup.find_all("link")
        assert len(link) == 0

        para = soup.find_all("p")

        assert para[0].text.startswith("Icon embedding example")
        error = para[0].find_all("pre")
        assert len(error) == 1
        assert "error" in error[0].attrs["class"]
        assert error[0].text == "circle-check.svg?"

        svg = para[0].find_all("svg")
        assert len(svg) == 0

        assert para[1].text.startswith("Icon embedding styling")
        error = para[1].find_all("pre")
        assert len(error) == 1
        assert "error" in error[0].attrs["class"]
        assert error[0].text == "circle-check.svg?"

        svg = para[0].find_all("svg")
        assert len(svg) == 0

        # other examples using icons should still be issued, but will not draw correctly
        # as the stylesheets are missing in this example.
        assert para[2].text.startswith("Icon font-awesome example:")
        icon = para[2].find_all("i")
        assert len(icon) == 1
        assert icon[0].text == ""
        assert icon[0].attrs["class"] == ["fas", "fa-circle-check"]

        assert para[3].text.startswith("Icon bootstrap icons example:")
        icon = para[3].find_all("i")
        assert len(icon) == 1
        assert icon[0].text == ""
        assert icon[0].attrs["class"] == ["bi", "bi-check-circle"]

    _check_article(pelican_output / "article-rst.html")
    _check_article(pelican_output / "article-markdown.html")

    _assert_log_contains(
        records,
        message="Cannot find file `circle-check.svg`",
        level=logging.ERROR,
        count=4,
    )
