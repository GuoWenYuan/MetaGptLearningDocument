from pathlib import Path
from my_tests.Game_Agent.common import ShareBlackBoard,Const
from docx import Document
from metagpt.actions import Action
from metagpt.logs import logger
import asyncio

class CollectIdea(Action):
    """收集想法的Action"""

    async def run(self, idea):
        content = await self._aask(f"帮我在网络中收集：{idea}的相关信息,总结并返回给我")
        print(content)
        return content



asyncio.run(CollectIdea().run("2023年中国热门小说排行"))