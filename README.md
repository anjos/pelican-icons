<!--
SPDX-FileCopyrightText: Copyright © 2024 André Anjos <andre.dos.anjos@gmail.com>
SPDX-License-Identifier: MIT
-->

[![Build Status](https://img.shields.io/github/actions/workflow/status/anjos/pelican-icons/main.yml?branch=main)](https://github.com/anjos/pelican-icons/actions)
[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/anjos/pelican-icons/python-coverage-comment-action-data/endpoint.json&label=coverage)](https://htmlpreview.github.io/?https://github.com/anjos/pelican-icons/blob/python-coverage-comment-action-data/htmlcov/index.html)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-icons)](https://pypi.org/project/pelican-icons/)
[![Downloads](https://img.shields.io/pypi/dm/pelican-icons)](https://pypi.org/project/pelican-icons/)
![License](https://img.shields.io/pypi/l/pelican-icons?color=blue)

# icons: A Plugin for Pelican

This plugin simplifies adding SVG or webfont icons on your Pelican website content
(pages and articles).

## Installation

This plugin can be installed via:

```sh
pip install pelican-icons
````

This a "namespace plugin" for Pelican.  After installation, it should be automatically
detected.  It is enabled by default if `PLUGINS` is not set on your configuration.  In
case that variable is set, add `icons` to the list of plugins to load. For more
information, check [How to Use
Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins)
documentation.

## Usage

There are 2 techniques implemented in this plugin to use icons in your article and
pages, [each with particular advantages](https://blog.fontawesome.com/webfont-vs-svg/).

### Technique 1: Embedding SVG icons

To embed SVG icons directly on your articles and pages, copy SVG files under a path
indicated by the configuration variable `ICONS_SVG_PATH` (default: `svg`), then simply
refer to the files by name (relative path, and without the `.svg` extension) on your
articles.

In RST articles and pages, use something like:

```rst
:svg:`fa/circle-check`, to load the contents from `<ICONS_SVG_PATH>/fa/circle-check.svg`.
```

In Markdown articles and pages, use something like:

```md
{svg}`fa/circle-check`, to load the contents from `<ICONS_SVG_PATH>/fa/circle-check.svg`.
```

This will cause the SVG file to be directly embedded in the output HTML page for content
in question, generating something like:

```html
<svg aria-hidden="true" focusable="false" class="icon" fill="currentColor" width="1em" height="1em">...</svg>
```

Note that by default, SVG icons are embedded in HTML with the following attributes:

```python
{
    "aria-hidden": "true",
    "focusable": "false",
    "fill": "currentColor",
    "width": "1em",
    "height": "1em",
}
```

This typically makes the icon match the size and color of the surrounding text, **for as
long as the original SVG file root element or sub-elements do not override the attribute
`fill`**.  In such cases, it is recommended you edit the SVG file, either manually or
automatically to remove such hard-coded values.

#### Coloring and re-sizing

To change the color and resize the inserted icon, or modify other SVG tag attributes,
simply use the alternate syntax below:

```rst
:svg:`fa/circle-check{"fill":"red"}` is a red circle

:svg:`fa/circle-check{"width":"2em","height":"2em"}` is a large circle

:svg:`fa/circle-check{"fill":"green","width":"3em","height":"3em"}` is an even larger green circle
```

In Markdown articles and pages, use:

```md
{svg}`fa/circle-check{"fill":"red"}` is a red circle

{svg}`fa/circle-check{"width":"2em","height":"2em"}` is a large circle

{svg}`fa/circle-check{"fill":"green","width":"3em","height":"3em"}` is an even larger green circle
```

> Implementation note:  The above alternate syntax modifies the `svg` tag attribute for
> the inserted icon.  Any attribute that can go into an `svg` tag can be set or
> overriden using this technique. The contents within braces should be a JSON-parseable
> dictionary containing the attributes you would like to override.

#### Obtaining SVG icons

There are various open-source and free repositories with SVG icons you can use on your
Pelican website.  Some of them are listed below:

* Font-awesome: <https://github.com/FortAwesome/Font-Awesome>
* Boostrap: <https://github.com/twbs/icons/releases/>
* Material design: <https://github.com/Templarian/MaterialDesign>
* Material design light: <https://github.com/Pictogrammers/MaterialDesignLight>
* Tabler icons: <https://github.com/tabler/tabler-icons>
* Twitter Emoji: <https://github.com/twitter/twemoji>

### Technique 2: Using webfonts

You may also display icons use
[webfonts](https://fonts.google.com/knowledge/glossary/web_font). The main advantage of
this approach compared to the direct SVG icon injection above is that font files can be
cached, potentially speeding up load times.

The process of using a webfont for icon drawing on HTML is composed of 2 parts: a)
injecting one or more CSS files on HTML pages, and then b) adding `i` or `span` elements
to your content using pre-defined stylesheet classes. Next we explain how to achieve
this within Pelican via this plugin. The process is composed of 3 steps: 1) adjust your
configuration to list all CSS sources that must be included on your templates; 2) modify
your templates to inject the configured CSS sources; 3) refer to icons on your content.

#### Step 1: Adjust configuration

There are 2 ways to list the required CSS so that you can refer to webfont icons on your
content: 1a) shipping yourself CSS and webfont files, or 1b) using a content
distribution network (CDN). You can mix and match as required. However, if you are
shipping yourself the CSS and webfont files, you will need to modify your
`pelicanconf.py` so that those files are copied to the output directory.  For example:

```python
# Place all resources to be copied verbatim at one of the STATIC_PATHS.
# For example, download font-awesome files at "fonts/font-awesome" and
# bootstrap-icons at "fonts/bootstrap".
# Reference: https://docs.getpelican.com/en/latest/settings.html
STATIC_PATHS = ["fonts"]
```

In the next step we explain how to inject the CSS sources listed above on your theme
templates.

#### Step 2: Injecting required CSS sources

Pelican uses a templating engine to generate HTML pages. It is therefore easier to
change the base templates to inject the required CSS code enabling icon drawing from
webfonts.

Because of programmatic differences between various Pelican themes, CSS injection
remains theme-specific and may require overwriting one (e.g. `base.html`) or more theme
templates. Refer to the [Pelican documentation of
`THEME_TEMPLATES_OVERRIDES`](https://docs.getpelican.com/en/latest/settings.html) for
details on how to do this). For the standard themes "simple" or "notmyidea", which are
shipped with Pelican itself, this is rather trivial: override the head block on
`base.html` to link a new stylesheet. For example:

```html
{% extends "!simple/base.html" %}

{% block head %}
{{ super() }}

  <!-- link stylesheets as required by the webfont -->

  <!-- example for free version of fontawesome, shipped on own website, use instead of the one below -->
  <link rel="stylesheet" type="text/css" href="/font-awesome/css/fontawesome.min.css" />
  <link rel="stylesheet" type="text/css" href="/font-awesome/css/solid.min.css" />
  <link rel="stylesheet" type="text/css" href="/font-awesome/css/brands.min.css" />

  <!-- example for free version of fontawesome, from CDN, use instead of the one above -->
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.7.0/css/fontawesome.min.css" />
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.7.0/css/solid.min.css" />
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.7.0/css/brands.min.css" />

  <!-- example for bootstrap-icons, shipped on own website, use instead of the one below -->
  <link rel="stylesheet" type="text/css" href="/bootstrap/bootstrap-icons.min.css" />

  <!-- example for bootstrap-icons, from CDN, use instead of the one above -->
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" />

{% endblock %}
```

Create the file at `templates/base.html` with the (some of the) above contents, then set
`THEME=simple` and `THEME_TEMPLATES_OVERRIDES="templates"` at `pelicanconf.py`. Adjust
if you are using another theme. Refer to the theme's user guide for details on how to
achieve this.

#### Step 3: Using icons on your content

In RST articles and pages, use something like `:icon:<class1> <class2> .. <classN>` like so:

```rst
:icon:`fa-solid fa-circle-check`, to print a check in a circle with font-awesome icons.

:icon:`bi bi-check-circle`, to print a check in a circle with boostrap icons.
```

In Markdown articles and pages, use something like `{icon}<class1> <class2> ... <class N>` like so:

```md
{icon}`fa-solid fa-circle-check`, to print a check in a circle with font-awesome icons.

{icon}`bi bi-check-circle`, to print a check in a circle with boostrap icons.
```

Refer to the documention of the webfont to correctly select the classes related to the
icons of interest.

The above syntax is transformed into an output that looks like:

```html
<i class="bi bi-check-circle"></i>
```

#### Coloring and re-sizing

To change the color and resize the inserted icon, so it is different than the
surrounding text, simply use the alternate syntax:

```rst
:icon:`fa-solid fa-circle-check{"color":"red"}` is a red circle

:icon:`fa-solid fa-circle-check{"font-size":"2em"}` is a large circle

:icon:`fa-solid fa-circle-check{"color":"green","font-size":"3em"}` is an even larger green circle
```

In Markdown articles and pages, use:

```md
{icon}`fa-solid fa-circle-check{"color":"red"}` is a red circle

{icon}`fa-solid fa-circle-check{"font-size":"2em"}` is a large circle

{icon}`fa-solid fa-circle-check{"color":"green","font-size":"3em"}` is an even larger green circle
```

The above syntax produces something like:

```html
<span style="color: green; font-size: 3em;"><i class="bi bi-check-circle"></i></span>
```

> Implementation note: The above alternate syntax surrounds the output `i` tag attribute
> for the inserted icon with a styled `span` tag.  Any key-value pair that can appear on
> the `style` attribute can be set using this technique. The contents within braces
> should be a JSON-parseable dictionary containing the attributes you would like to
> override.

#### Obtaining icon webfonts

There are various open-source and free repositories with web fonts you can use on your
Pelican website.  Some of them are listed below:

* Font-awesome: <https://github.com/FortAwesome/Font-Awesome> (or via CDN at <https://www.bootstrapcdn.com>)
* Boostrap icons: <https://github.com/twbs/icons/releases/> (or via CDN at <https://www.bootstrapcdn.com>)
* Material design: <https://github.com/Templarian/MaterialDesign>
* Material design light: <https://github.com/Pictogrammers/MaterialDesignLight>
* Tabler icons: <https://github.com/tabler/tabler-icons>

## Contributing

Contributions are welcome and appreciated. Every little bit helps. You can
contribute by improving the documentation, adding missing features, and fixing bugs. You
can also help out by reviewing and commenting on [existing
issues](https://github.com/anjos/pelican-icons/issues).

To start contributing to this plugin, review the [Contributing to
Pelican](https://docs.getpelican.com/en/latest/contribute.html) documentation, beginning
with the **Contributing Code** section.

## License

This project is licensed under the MIT license.
