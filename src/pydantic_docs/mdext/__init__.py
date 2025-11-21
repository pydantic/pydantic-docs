from typing import Any

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor

from .public_trace import PublicTrace
from .versioning import VersionAdded, VersionChanged, VersionDeprecated, VersionDeprecatedRemoved


class PydanticDocsExtension(BlocksExtension):
    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(PublicTrace, self.getConfigs())
        block_mgr.register(VersionAdded, self.getConfigs())
        block_mgr.register(VersionChanged, self.getConfigs())
        block_mgr.register(VersionDeprecated, self.getConfigs())
        block_mgr.register(VersionDeprecatedRemoved, self.getConfigs())


def makeExtension(*args: Any, **kwargs: Any) -> PydanticDocsExtension:
    """Return extension."""

    return PydanticDocsExtension(*args, **kwargs)
