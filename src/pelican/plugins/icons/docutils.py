# SPDX-FileCopyrightText: Copyright © 2024 André Anjos <andre.dos.anjos@gmail.com>
#
# SPDX-License-Identifier: MIT
"""Docutils role inliner."""

import logging
import pathlib
import typing
import xml.etree.ElementTree as ET

import docutils.nodes
import docutils.parsers.rst.states

import pelican

from . import utils

logger = logging.getLogger(__name__)


class IconInliner:
    """Replaces inline roles by appropriate HTML tags."""

    def __init__(self):
        pass

    def init(self, pelican_object: pelican.Pelican):
        """Initialize this inliner.

        Parameters
        ----------
        pelican_object
            Pelican main object, including the configuration.
        """
        self.basepath = pathlib.Path(
            pelican_object.settings.get("ICONS_SVG_PATH", "svg")
        )

    def svg(  # noqa: PLR0913
        self,
        name: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: docutils.parsers.rst.states.Inliner,
        options: typing.Mapping[str, typing.Any] = {},
        content: typing.Sequence[str] = [],
    ) -> tuple[
        typing.Sequence[docutils.nodes.reference],
        typing.Sequence[docutils.nodes.reference],
    ]:
        """Add embedded-SVG icons to HTML output.

        Reference: https://docutils.sourceforge.io/docs/howto/rst-roles.html

        Parameters
        ----------
        name
            The local name of the interpreted role, the role name actually used in the
            document. (example: ``svg``).
        rawtext
            A string containing the entire interpreted text input, including the role
            and markup. Return it as a problematic node linked to a system message if a
            problem is encountered. (example: ``:svg:'data'``).
        text
            The interpreted text content. (example: ``data``).
        lineno
            The line number where the text block containing the interpreted text begins.
        inliner
            The docutils.parsers.rst.states.Inliner object that called role_fn. It
            contains the several attributes useful for error reporting and document tree
            access.
        options
            A dictionary of directive options for customization (from the "role"
            directive), to be interpreted by the role function. Used for additional
            attributes for the generated elements and other functionality.
        content
            A list of strings, the directive content for customization (from the "role"
            directive). To be interpreted by the role function.

        Returns
        -------
            Role functions return a tuple of two values:

            * A sequence of nodes which will be inserted into the document tree at the point
            where the interpreted role was encountered (can be an empty list).
            * A sequence of system messages, which will be inserted into the document
            tree immediately after the end of the current block (can also be empty).
        """
        del rawtext, lineno, inliner, options, content  # shuts-up linter
        assert name == "svg"
        xml = utils.load_svg_icon(text, self.basepath)
        return [
            docutils.nodes.raw(  # type: ignore[list-item]
                "",
                ET.tostring(xml, encoding="unicode", short_empty_elements=False),
                format="html",
            )
        ], []

    def icon(  # noqa: PLR0913
        self,
        name: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: docutils.parsers.rst.states.Inliner,
        options: typing.Mapping[str, typing.Any] = {},
        content: typing.Sequence[str] = [],
    ) -> tuple[
        typing.Sequence[docutils.nodes.reference],
        typing.Sequence[docutils.nodes.reference],
    ]:
        """Add webfont-referenced SVG icons to HTML output.

        Reference: https://docutils.sourceforge.io/docs/howto/rst-roles.html

        Parameters
        ----------
        name
            The local name of the interpreted role, the role name actually used in the
            document. (example: ``icon``).
        rawtext
            A string containing the entire interpreted text input, including the role
            and markup. Return it as a problematic node linked to a system message if a
            problem is encountered. (example: ``:svg:'data'``).
        text
            The interpreted text content. (example: ``data``).
        lineno
            The line number where the text block containing the interpreted text begins.
        inliner
            The docutils.parsers.rst.states.Inliner object that called role_fn. It
            contains the several attributes useful for error reporting and document tree
            access.
        options
            A dictionary of directive options for customization (from the "role"
            directive), to be interpreted by the role function. Used for additional
            attributes for the generated elements and other functionality.
        content
            A list of strings, the directive content for customization (from the "role"
            directive). To be interpreted by the role function.

        Returns
        -------
            Role functions return a tuple of two values:

            * A sequence of nodes which will be inserted into the document tree at the point
            where the interpreted role was encountered (can be an empty list).
            * A sequence of system messages, which will be inserted into the document
            tree immediately after the end of the current block (can also be empty).
        """
        del rawtext, lineno, inliner, options, content  # shuts-up linter
        assert name == "icon"
        xml = utils.make_webfont_icon(text)
        return [
            docutils.nodes.raw(  # type: ignore[list-item]
                "",
                ET.tostring(xml, encoding="unicode", short_empty_elements=False),
                format="html",
            )
        ], []
