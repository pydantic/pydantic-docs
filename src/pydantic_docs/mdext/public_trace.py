import xml.etree.ElementTree as etree
from typing import Any, Literal, cast
from urllib.parse import urlparse

from pymdownx.blocks.block import Block, type_string, type_string_in

# Source: https://raw.githubusercontent.com/squidfunk/mkdocs-material/aee925f5/material/templates/.icons/octicons/link-external-16.svg
LINK_EXTERNAL_16_SVG = '<svg viewBox="0 0 16 16"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2m6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.75.75 0 0 1-1.042-.018.75.75 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1"/></svg>'  # noqa: E501


def validate_public_trace_url(value: Any) -> str:
    v = type_string(value)
    try:
        parsed = urlparse(v)
    except ValueError as e:
        raise ValueError(f'Could not parse {v} as an URL') from e

    if parsed.netloc not in ('logfire-us.pydantic.dev', 'logfire-eu.pydantic.dev'):
        raise ValueError(f'{v} is not a public trace URL')

    return v


class PublicTrace(Block):
    """A block generating an iframe for a public trace."""

    NAME = 'public-trace'
    ARGUMENT = True  # Public trace URL
    OPTIONS = {  # noqa: RUF012
        'title': ('', type_string),
        'caption': ('append', type_string_in(['off', 'append', 'prepend'])),
        'loading': ('lazy', type_string_in(['lazy', 'eager'])),
    }

    url: str

    def on_validate(self, parent: etree.Element) -> bool:
        try:
            self.url = validate_public_trace_url(self.argument)
        except ValueError:
            return False

        return True

    def on_create(self, parent: etree.Element) -> etree.Element:
        title = cast(str, self.options['title'])
        caption = cast(Literal['off', 'append', 'prepend'], self.options['caption'])
        loading = cast(Literal['lazy', 'eager'], self.options['loading'])
        url = self.url

        div_element = etree.SubElement(parent, 'div')
        if caption != 'off':
            figure_element = etree.SubElement(div_element, 'figure', {'style': 'width: 100%;'})
        else:
            figure_element = div_element

        # Guaranteed to parse successfully thanks to validation:
        parsed = urlparse(url)
        if not parsed.query:
            query = 'embedded=true'
        else:
            query = f'{parsed.query}&embedded=true'
        src = parsed._replace(query=query).geturl()

        iframe_element = etree.SubElement(
            figure_element,
            'iframe',
            {'src': src, 'style': 'aspect-ratio: 16 / 9; height: 100%; width: 100%;', 'loading': loading},
        )
        if title:
            iframe_element.set('title', title)

        if caption != 'off':
            if caption == 'prepend':
                figcaption_element = etree.Element('figcaption')
                figure_element.insert(0, figcaption_element)
            else:
                figcaption_element = etree.SubElement(figure_element, 'figcaption')

            p_element = etree.SubElement(figcaption_element, 'p')
            if title:
                p_element.text = f'{title} — '

            a_element = etree.SubElement(p_element, 'a', {'href': url})
            a_element.text = 'View in Logfire '
            span_element = etree.SubElement(a_element, 'span', {'class': 'twemoji'})
            svg_element = etree.fromstring(LINK_EXTERNAL_16_SVG)
            svg_element.set('xmlns', 'http://www.w3.org/2000/svg')
            span_element.append(svg_element)

        return div_element
