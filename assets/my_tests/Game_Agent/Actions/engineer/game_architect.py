# -*- coding: utf-8 -*-
from pathlib import Path
from my_tests.Game_Agent.common import ShareBlackBoard,Const
from docx import Document
from metagpt.actions import Action
from metagpt.logs import logger
import asyncio
import re
import os

class GameArchitectAction(Action):

    async def run(self, doc_path):
        prompt = self._get_prompt()
        doc_content = self._get_doc(doc_path)
        prompt = prompt.replace(Const.DesignDoc, doc_content)
        doc = await self._aask(prompt)
        #收到信息后保存到当前文件目录中
        self._save(os.path.basename(doc_path), doc)
        ShareBlackBoard.save_doc(Const.DesignDoc, doc_content)
        return doc

    def _save(self, file_name, content):
        """保存文档"""
        ShareBlackBoard.save_to_blackboard({Const.FileName: file_name})
        ShareBlackBoard.save_doc(Const.Document,content)
        #self._save_architecture_diagram(content)





    def _get_prompt(self):
        prompt_name = self._get_file_path().name.split('.')[0] + '.txt'
        with open(f'{self._get_dir_path()}/{prompt_name}',mode='r',encoding='utf-8') as f:
            return f.read()

    def _get_file_path(self):
        return Path(__file__).resolve()

    def _get_dir_path(self):
        return self._get_file_path().parent

    def _get_doc(self,doc_path):
        p = Document(doc_path)
        content = ''
        index = 0
        for i in p.paragraphs:
            if index > 10:
                content += i.text + '\n'
            index += 1
        logger.info(f"处理策划文档:{doc_path}")
        ShareBlackBoard.save_doc(Const.DesignDoc, content)
        return content


#asyncio.run(GameArchitectAction().run(doc))


ShareBlackBoard.save_task("Rider")
asyncio.run(GameArchitectAction().run("C:/Game/PC_Creative/X_系统/需求设计文档/02 正式版本需求/051 坐骑/坐骑V1.1.docx"))

