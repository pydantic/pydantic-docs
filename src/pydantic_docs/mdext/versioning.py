import xml.etree.ElementTree as etree
from typing import ClassVar

from pymdownx.blocks.block import Block


class VersionChange(Block):
    """A block generating an iframe for a public trace."""

    ARGUMENT = True  # Version

    LABEL: ClassVar[str]
    """
    The label to use, e.g. 'Added in {arg[0]}', 'Deprecated in {arg[0]}'.

    `arg` is a list of strings, corresponding to the block argument, split by whitespace.
    """

    COLOR: ClassVar[str]
    """The CSS color to use for the label."""

    def on_create(self, parent: etree.Element) -> etree.Element:
        root_div = etree.SubElement(
            parent, 'div', {'style': f'border-left: .15rem solid {self.COLOR}; padding: 0 .5rem;'}
        )
        p_el = etree.SubElement(root_div, 'p')

        label_span_el = etree.SubElement(p_el, 'span', {'style': f'font-style: italic; color: {self.COLOR};'})
        label_span_el.text = f'{self.LABEL} {self.argument}'
        label_span_el.text = self.LABEL.format(arg=self.argument.split())

        # small_el = etree.SubElement(root_div, 'small', {'style': 'font-style: italic;'})

        # small_el.text = f"{self.LABEL} "
        # a_el = etree.SubElement(
        #     small_el,
        #     'a',
        #     {
        #         'href': f'https://github.com/pydantic/pydantic/releases/tag/{self.argument}',
        #         'target': '_blank',
        #     }
        # )
        # a_el.text = self.argument

        return root_div

    def on_end(self, block: etree.Element) -> None:
        # If the block has inner content, it is added as a `<p>` element. Change it to be a `<span>`
        # directly following the label. The following elements are added as is. Example:
        # /// version-added | v1
        # Info about addition.
        #
        # Other paragraph.
        # ///
        #
        # becomes:
        #
        # | Added in v1: Info about addition.
        # |
        # | Other paragraph.

        if len(block) >= 2:
            second_el = block[1]
            block.remove(second_el)
            second_el.tag = 'span'
            block[0].append(second_el)
            for el in block[2:]:
                block.remove(el)
                block[0].append(el)

            assert isinstance(block[0][0].text, str)  # The `label_span_el` content
            block[0][0].text += ': '
        else:
            assert isinstance(block[0][0].text, str)  # The `label_span_el` content
            block[0][0].text += '.'


class VersionAdded(VersionChange):
    NAME = 'version-added'
    LABEL = 'Added in {arg[0]}'
    COLOR = 'rgb(79, 196, 100)'


class VersionChanged(VersionChange):
    NAME = 'version-changed'
    LABEL = 'Changed in {arg[0]}'
    COLOR = 'rgb(244, 227, 76)'


class VersionDeprecated(VersionChange):
    NAME = 'version-deprecated'
    LABEL = 'Deprecated in {arg[0]}'
    COLOR = 'rgb(244, 76, 78)'


class VersionDeprecatedRemoved(VersionChange):
    NAME = 'deprecated-removed'
    LABEL = 'Deprecated in {arg[0]}, will be removed in version {arg[1]}'
    COLOR = 'rgb(244, 76, 78)'
