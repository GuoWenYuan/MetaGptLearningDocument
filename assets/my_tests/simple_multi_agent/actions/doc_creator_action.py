from metagpt.actions import Action

class DocCreatorAction(Action):
    name: str = "DocCreatorAction"
    prompt: str = """
    你的任务:
        你将会根据给定的代码内容，创建一个文档
        文档的格式为MarkDown格式
        
        文档应该包含内容:
        1.文件名称
        2.代码文件的精读与 相关代码块讲解
        3.代码文件中每个函数的详细解释
        4.代码文件中每个第三方库与语法糖的详细讲解
        
        你的约束:
        1.如果代码中相关的第三方库你不知道是什么，就不要写
        2.如果代码中相关的语法糖你不知道是什么，就不要写
        
        请注意:
        1.在MarkDown格式的文档中，每个代码块都应该有对应的解释
        2.对于代码块的解释，应该使用中文
        3.对于使用第三方库的代码，请给出第三方库的名称，以及相关代码块的讲解，并且对于第三方库中使用到的内容做详细的讲解，最好能给出例子
        
        用户的输入:{instruction}
        
        你的输出:
        直接返回makedown 文档
        
        使用中文
        
        
    """

    async def run(self, instruction: str):
        """获取instruction"""
        return await self._aask(self.prompt.replace('{instruction}', instruction))