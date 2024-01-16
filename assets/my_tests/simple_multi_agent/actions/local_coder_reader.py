from metagpt.actions import Action
import json
from metagpt.logs import logger
import asyncio

#官方教程地址:https://deepwisdom.feishu.cn/docx/RJmTdvZuPozAxFxEpFxcbiPwnQf
#我们尝试使用多agent的配合来完成理解metagpt代码中大量的python语法糖与第三方库的用法，由于对python不太熟悉，每次都要看语法糖与第三方库相关的东西太麻烦了，所以改下官方教程里的例子，变成我能用到的


class LocalCoderReader(Action):
    """获取本地的代码 ~

       Args:
           用于读取本地代码。
           参数：
           name：LocalCoderReader。
           language：输出的语言，默认为"Chinese"。
       这里并不需要他和llm产生直接交互，我们自己来读取代码内容即可
    """

    name: str = "LocalCoderReader"

    async def run(self, instruction: str):
        """instruction=本地需要理解代码的路径，为了方便我们定义格式，以;号来切分不同的路径（当然也可以用json，我只是单纯的懒）"""
        """这里取出记忆的时候取出的是rc的所有记忆，我们需要取出最近的一条数据"""

        code_paths = LocalCoderReader.split_path(instruction)
        resp = []
        for code_path in code_paths:
            with open(code_path, "r", encoding="utf-8") as f:
                #这里产生了问题，我们该以何种形式进行数据的返回?
                #思考后觉得使用json的格式  格式为[{code_name = 文件名称,code_path = 文件本地路径，code_content =  文件内容}]
                code_name = code_path.split("/")[-1]
                code_content = f.read()
                #转换为json格式返回
                json_data = json.dumps([{'code_name': code_name, 'code_path': code_path, 'code_content': code_content}])
                logger.info(f'本地代码读取完成:{json_data}')  # 这里使用metegpt的logger，info以上级别会在本地写入内容，方便看流程~
                resp.append(json_data)
        return json.dumps(resp)


    def split_path(code_paths:str):
        """按照;号切分路径"""
        if ';' in code_paths:
            return code_paths.split(";")
        return [code_paths]

#测试例子
#asyncio.run(LocalCoderReader().run("C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py;C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/roles/role.py"))
