from metagpt.actions import Action
import json
from metagpt.logs import logger
from typing import Optional
from pydantic import BaseModel, SkipValidation
import os
from os import path
import my_tests.simple_multi_agent.path as simple_path

class DocReviewAction(Action):
    """获取本地的代码 ~
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
        return self._review_doc(instruction)

    def _convert_to_json(self, msg):
        return json.loads(msg)

    def _review_doc(self,msg):
        """判断其他文档是否全部完成"""
        data = self._convert_to_json(msg)
        real_path = simple_path.get_doc_path()
        #遍历real_path 文件夹，获取所有文件名
        file_names = os.listdir(real_path)
        #去除file_names文件名称后缀
        file_names = [file_name.split('.')[0] for file_name in file_names]
        for doc_data in data:
            #print(f'我的data：{doc_data}')
            doc_data = json.loads(doc_data) #转换一下json
            doc_name = doc_data.get('code_name').split('.')[0]
            if doc_name not in file_names:
                self.create_doc_success = False
                return json.dumps(doc_data)
        self.create_doc_success = True
        return "create_doc_success"



