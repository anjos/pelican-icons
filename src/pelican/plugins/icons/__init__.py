# SPDX-FileCopyrightText: Copyright © 2024 André Anjos <andre.dos.anjos@gmail.com>
#
# SPDX-License-Identifier: MIT
"""Add HTML to content and templates."""

import importlib
import importlib.util
import logging

from .docutils import IconInliner as RSTIconInliner

logger = logging.getLogger(__name__)

_rst_inliner = RSTIconInliner()


def _get_rst_inliner_init(pelican_object):
    return _rst_inliner.init(pelican_object)


def _register_rst_svg(*args, **kwargs):
    return _rst_inliner.svg(*args, **kwargs)


def _register_rst_icon(*args, **kwargs):
    return _rst_inliner.icon(*args, **kwargs)


def register():
    """Register this plugin to pelican."""

    import docutils.parsers.rst.roles

    import pelican.plugins.signals

    pelican.plugins.signals.initialized.connect(_get_rst_inliner_init)

    docutils.parsers.rst.roles.register_local_role("svg", _register_rst_svg)
    docutils.parsers.rst.roles.register_local_role("icon", _register_rst_icon)

    if importlib.util.find_spec("markdown") is not None:
        from .markdown import setup_extension

        pelican.plugins.signals.initialized.connect(setup_extension)
    else:
        logger.warning("Markdown is not installed. Skip loading icon extension.")
