from metagpt.actions import Action
from metagpt.logs import logger
import os
import re
from my_tests.simple_multi_agent.path import get_doc_path

class WriteDocAction(Action):

    name: str = "WriteDocAction"

    async def run(self, file_name: str, instruction: str):
        """instruction=大模型返回的结果  file_name=要写入的文件名称"""
        real_path = f'{get_doc_path()}/{file_name}'

        with open(real_path, 'w', encoding='utf-8') as f:
            f.write(self._convert_markdown(instruction))
        logger.info(f"success write {file_name}")
        return f"success write {file_name}"

    def _convert_markdown(self, msg):
        """匹配markdown文件 返回格式为'''markdown''' xxxxx"""
        pattern = r'```markdown(.*)```'
        match = re.search(pattern, msg, re.DOTALL)
        code_text = match.group(1) if match else msg
        return code_text
