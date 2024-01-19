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
        你是一个精通python代码的程序员，并且有着丰富的编写技术文档的经验，能写出非常优秀的技术文档
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
        msg = await todo.run(instruction) #获取最近一条记忆，该记忆会从env publish_message 时放入
        logger.error(f'看我 to do message cause by  :{type(todo)}')
        return Message(content=msg, role=self.profile, cause_by=type(todo))





