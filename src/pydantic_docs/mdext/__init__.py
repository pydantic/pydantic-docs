from typing import Any

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor

from .public_trace import PublicTrace


class PydanticDocsExtension(BlocksExtension):
    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(PublicTrace, self.getConfigs())


def makeExtension(*args: Any, **kwargs: Any) -> PydanticDocsExtension:
    """Return extension."""

    return PydanticDocsExtension(*args, **kwargs)
