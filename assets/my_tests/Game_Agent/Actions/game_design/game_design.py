from metagpt.actions import Action
from docx import Document
from metagpt.logs import logger
from my_tests.Game_Agent.common import get_prompt, ShareBlackBoard,Const
import asyncio

class ActionGameDesign(Action):
    """读取本地策划文档"""

    async def run(self, doc_path):
        """读取策划文档"""
        design_content = self._get_design_doc(doc_path)
        prompt = get_prompt('prompt').replace(Const.DesignDoc,design_content)
        logger.info(f'处理策划文档prompt:{prompt}')
        new_design = await self._aask(prompt)
        logger.info(f'最终处理完成文档:{new_design}')
        ShareBlackBoard.save_doc(f'{Const.DesignDoc}.txt',new_design)
        return new_design

    def _get_design_doc(self,doc_path):
        p = Document(doc_path)
        content = ''
        index = 0
        for i in p.paragraphs:
            if index > 10:
                content += i.text + '\n'
            index += 1
        logger.info(f"处理策划文档:{doc_path}")
        return content


ShareBlackBoard.save_task('策划行为测试')
asyncio.run(ActionGameDesign().run('C:/Game/PC_Creative/X_系统/需求设计文档/02 正式版本需求/051 坐骑/坐骑V1.1.docx'))