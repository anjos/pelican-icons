# SPDX-FileCopyrightText: Copyright © 2024 André Anjos <andre.dos.anjos@gmail.com>
#
# SPDX-License-Identifier: MIT
"""Markdown inline processor."""

import pathlib
import re
import typing
import xml.etree.ElementTree as ET

import markdown.core
import markdown.extensions
import markdown.inlinepatterns

import pelican

from . import utils


class IconSVGInlineProcessor(markdown.inlinepatterns.InlineProcessor):
    """Transform SVG icon annotations into HTML.

    Parameters
    ----------
    pattern
        The pattern we are matching.
    md
        The markdown parser.
    basepath
        The base path where SVG icons are installed.
    """

    def __init__(
        self,
        pattern: str,
        md: typing.Union[markdown.core.Markdown, None],
        basepath: pathlib.Path,
    ):
        self.basepath = basepath
        super().__init__(pattern, md)

    def handleMatch(  # type: ignore[override]  # noqa: N802
        self, m: re.Match[str], data: str
    ) -> tuple[
        typing.Union[ET.Element, str, None],
        typing.Union[int, None],
        typing.Union[int, None],
    ]:
        del data
        el = utils.load_svg_icon(m.group(1), self.basepath)

        # Comments in SVG icons will cause problems, and often SVG artwork available
        # contains copyright and licensing commands we'd like to keep on the produced
        # HTML.  We check for this and use the special htmlStash to keep this value
        # untouched
        for child in list(el):
            if not isinstance(child.tag, str):
                el.remove(child)

        return el, m.start(0), m.end(0)


class IconFontInlineProcessor(markdown.inlinepatterns.InlineProcessor):
    """Transform Webfont icon annotations into HTML."""

    def handleMatch(  # type: ignore[override]  # noqa: N802
        self, m: re.Match[str], data: str
    ) -> tuple[
        typing.Union[ET.Element, str, None],
        typing.Union[int, None],
        typing.Union[int, None],
    ]:
        del data
        el = utils.make_webfont_icon(m.group(1))
        return el, m.start(0), m.end(0)


class IconExtension(markdown.extensions.Extension):
    """Extend markdown to support SVG icon annotations (``{svg}`name```).

    Parameters
    ----------
    **kwargs
        Assorted keyword parameters to be passed up to the parent's constructor.
    """

    def __init__(self, **kwargs):
        self.config = {"basepath": [kwargs["basepath"], "Basepath to SVG static files"]}
        super().__init__(**kwargs)

    def extendMarkdown(self, md: markdown.core.Markdown):  # noqa: N802
        pattern = r"{svg}`(.*)`"  # like {svg}`circle-check`
        md.inlinePatterns.register(
            IconSVGInlineProcessor(pattern, md, self.config["basepath"][0]), "svg", 999
        )

        pattern = r"{icon}`(.*)`"  # like {icon}`fa-regular fa-circle-check`
        md.inlinePatterns.register(IconFontInlineProcessor(pattern, md), "icon", 999)


def setup_extension(pelican_object: pelican.Pelican):
    """Set up markdown extension.

    Parameters
    ----------
    pelican_object
        The pelican object with settings.
    """
    mdsettings = pelican_object.settings.get("MARKDOWN", {})
    configs: dict[str, dict[str, typing.Any]] = mdsettings.get("extension_configs", {})
    configs[f"{__name__}:IconExtension"] = {
        "basepath": pelican_object.settings.get("ICONS_SVG_PATH", pathlib.Path("svg"))
    }
