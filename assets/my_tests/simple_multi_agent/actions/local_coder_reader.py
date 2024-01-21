from metagpt.actions import Action
import json
from metagpt.logs import logger
import asyncio


class LocalCoderReader(Action):
    """获取本地的代码"""

    name: str = "LocalCoderReader"

    async def run(self, instruction: str):
        """instruction=本地需要理解代码的路径，为了方便我们定义格式，以;号来切分不同的路径（可以使用文件目录或者相关数据结构~）"""
        """这里取出记忆的时候取出的是rc的所有记忆，我们需要取出最近的一条数据"""

        code_paths = LocalCoderReader.split_path(instruction)
        resp = []
        for code_path in code_paths:
            with open(code_path, "r", encoding="utf-8") as f:
                #[{code_name = 文件名称,code_path = 文件本地路径，code_content =  文件内容}]
                code_name = code_path.split("/")[-1]
                code_content = f.read()
                #转换为json格式返回
                json_data = json.dumps({'code_name': code_name, 'code_path': code_path, 'code_content': code_content},ensure_ascii=False)
                resp.append(json_data)
        return json.dumps(resp)


    def split_path(code_paths:str):
        """按照;号切分路径"""
        if ';' in code_paths:
            return code_paths.split(";")
        return [code_paths]

