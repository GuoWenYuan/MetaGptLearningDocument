from metagpt.actions import Action
import json
from metagpt.logs import logger
from typing import Optional
from pydantic import BaseModel, SkipValidation
import os
from os import path
import my_tests.simple_multi_agent.path as simple_path

class DocReviewAction(Action):
    """PM通知其他模块进行处理 ~
          不需要与LLM进行交互
          Args:
              用于审核内容是否全部完成。
              参数：
              name：CoderToolContentReview。
              language：输出的语言，默认为"Chinese"。
       """

    name: str = "CoderToolContentReview"
    create_doc_success: bool = False

    async def run(self, instruction: str):
        """获取instruction"""
        return instruction





