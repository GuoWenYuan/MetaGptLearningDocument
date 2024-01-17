import json

from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from my_tests.simple_multi_agent.actions import DocReviewAction,DocCreatorAction

class DocCreatorRole(Role):
    """创建文档的角色"""

    name: str = "DocCreatorRole"
    profile: str = "DocCreatorRole"
    prompt: str = """
        你的角色:
        你是一个精通python代码，并可以写成非常优秀文档的程序员
    """


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._set_react_mode("by_order")
        self.init_actions([DocCreatorAction])
        self._watch([DocReviewAction])

    async def _act(self) -> Message:
        todo = self.rc.todo
        #写入角色
        todo.set_prefix(self.prompt)
        instruction = self.get_memories(k=1)[0].content
        file_name = json.loads(instruction).get('code_name').split('.')[0]+'.md'
        #self.rc.memory.add(Message(content=file_name, role=self.profile, cause_by=type(todo)))
        #logger.info(f"文件名称:{file_name}")
        msg = await todo.run(instruction) #获取最近一条记忆，该记忆会从env publish_message 时放入

        return Message(content=msg,role=self.profile,cause_by=type(todo))





