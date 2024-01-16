from metagpt.actions import Action
import json
from metagpt.logs import logger
from typing import Optional
from pydantic import BaseModel, SkipValidation
class CoderToolContentReview(Action):
    """获取本地的代码 ~
          不需要与LLM进行交互
          Args:
              用于审核内容是否全部完成。
              参数：
              name：CoderToolContentReview。
              language：输出的语言，默认为"Chinese"。
       """

    name: str = "CoderToolContentReview"
    #review_content_data: SkipValidation[any]


    async def run(self, instruction: str):
        """获取instruction"""
        print(f'CoderToolContentReview:{instruction}')
        #self.review_content_data = json.loads(instruction)
        #logger.info(self.review_content_data)
        return instruction