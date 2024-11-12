# SPDX-FileCopyrightText: Copyright © 2024 André Anjos <andre.dos.anjos@gmail.com>
#
# SPDX-License-Identifier: MIT
"""Common utilities for both rst and markdown documents."""

import json
import logging
import pathlib
import re
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

SVG_ICON_RE = re.compile(r"([^\{]+)(\{.*\}){1}")


def _parse_value_and_dict(text: str) -> tuple[str, dict[str, str]]:
    """Parse ``value{"key1":"val1",...}`` into str and dict.

    Parameters
    ----------
    text
        The text to parse.

    Returns
    -------
        The string before the curly-brace start and a dictionary formed by parsing the
        contents of the curly-brace-d section.
    """

    user_attrs_match = SVG_ICON_RE.match(text)

    d: dict[str, str] = {}
    if user_attrs_match is not None:
        s = user_attrs_match.group(1)
        try:
            d = json.loads(user_attrs_match.group(2))
        except json.decoder.JSONDecodeError:
            logger.exception(f"Error parsing `{user_attrs_match.group(2)}`")
    else:
        s = text

    return s, d


def load_svg_icon(stem: str, basepath: pathlib.Path) -> ET.Element:
    """Load an SVG icon from a file as an XML ElementTree document.

    Parameters
    ----------
    stem
        The filename stem to search for.
    basepath
        The basepath where icons are installed.

    Returns
    -------
        The SVG root element of the SVG icon, ready for insertion at a document tree.
    """

    user_attrs = {
        "aria-hidden": "true",
        "focusable": "false",
        "fill": "currentColor",
        "width": "1em",
        "height": "1em",
    }

    filename, user_attrs_override = _parse_value_and_dict(stem)
    user_attrs.update(user_attrs_override)

    # check that the file exists on the pre-configured directory
    if not filename.endswith(".svg"):
        filename += ".svg"

    filepath = basepath / filename

    if not filepath.exists():
        logger.error(f"Cannot find file `{filename}` (`{filepath}`?)")
        error = ET.Element("pre", attrib={"class": "error"})
        error.text = f"{filename}?"
        return error

    # load the file contents
    logger.info(f"Loading contents of file `{filename}` (`{filepath}`)...")
    ctb = ET.TreeBuilder(insert_comments=True)
    xp = ET.XMLParser(target=ctb)
    contents = ET.parse(filepath, parser=xp)
    svg = contents.getroot()
    assert svg.tag.endswith("svg")

    # resets the xmlns to reside within the tag so serliazation is correct for HTML
    # embedding
    namespace_re = re.compile("^{(.*)}(.*)$")
    for k in [svg, *list(svg)]:
        if not isinstance(k.tag, str):
            # probably a comment
            continue

        match = namespace_re.match(k.tag)
        if match:
            k.tag = match.group(2)
            k.attrib["xmlns"] = match.group(1)

    # modifies the loaded SVG to prepare for HTML insertion
    svg.attrib.update(user_attrs)

    return svg


def make_webfont_icon(text: str) -> ET.Element:
    """Create an HTML entry for a webfont-based icon.

    Parameters
    ----------
    text
        The class and style of the icon to be created.

    Returns
    -------
        The root element of the icon, ready for insertion at a document tree.
    """

    classes, style = _parse_value_and_dict(text)

    i = ET.Element("i", {"class": classes})

    if style:
        span = ET.Element(
            "span", {"style": "; ".join([f"{k}: {v}" for k, v in style.items()]) + ";"}
        )
        span.append(i)
        return span

    return i
