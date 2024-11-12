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
    """Transform SVG icon annotations into HTML."""

    def __init__(
        self, pattern: str, md: markdown.core.Markdown, basepath: pathlib.Path
    ):
        self.basepath = basepath
        super().__init__(pattern, md)

    def handleMatch(self, m: re.Match, data: str) -> tuple[ET.Element, int, int]:  # noqa: N802
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

    def handleMatch(self, m: re.Match, data: str) -> tuple[ET.Element, int, int]:  # noqa: N802
        del data
        el = utils.make_webfont_icon(m.group(1))
        return el, m.start(0), m.end(0)


class IconExtension(markdown.extensions.Extension):
    """Extend markdown to support SVG icon annotations (``{svg}`name```)."""

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
        The pelican object with settings.
    """
    mdsettings = pelican_object.settings.get("MARKDOWN", {})
    configs: dict[str, dict[str, typing.Any]] = mdsettings.get("extension_configs", {})
    configs[f"{__name__}:IconExtension"] = {
        "basepath": pelican_object.settings.get("ICONS_SVG_PATH", pathlib.Path("svg"))
    }
