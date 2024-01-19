from metagpt.actions import Action
import json
from metagpt.logs import logger
import os
import re
from my_tests.simple_multi_agent.path import get_doc_path

class WriteDocAction(Action):

    name: str = "WriteDocAction"

    async def run(self, file_name: str, instruction: str):
        """instruction=大模型返回的结果，我们从中提取出需要的信息，file_name = 本地写入的文件名称  content = 本地写入的内容"""
        """这里取出记忆的时候取出的是rc的所有记忆，我们需要取出最近的一条数据"""
        real_path = f'{get_doc_path()}/{file_name}'

        with open(real_path, 'w', encoding='utf-8') as f:
            f.write(self._convert_markdown(instruction))
        #这里还有一种方式是返回文件名称，在DocReviewRole检测文件是否写完时直接获取WriteDocRole记忆中的所有已经写入的文件内容
        logger.info(f"success write {file_name}")
        return f"success write {file_name}"

    def _convert_markdown(self,msg):
        """匹配json文件 返回格式为'''markdown''' xxxxx"""
        pattern = r'```markdown(.*)```'
        #logger.info(f"处理的json字段：{msg}")
        match = re.search(pattern, msg, re.DOTALL)
        code_text = match.group(1) if match else msg
        return code_text
