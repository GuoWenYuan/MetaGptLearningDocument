import asyncio
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from my_tests.simple_multi_agent.actions import DocCreatorAction,WriteDocAction
import my_tests.simple_multi_agent.path as path
class WriteDocRole(Role):

    name: str = "WriteDocRole"
    profile: str = "WriteDocRole"

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([DocCreatorAction])
        self._set_react_mode("by_order") #不需要与大模型进行交互
        self.init_actions([WriteDocAction])

    async def _act(self) -> Message:
        logger.info(f'开始写入本地文件')
        todo = self.rc.todo
        doc_name = self.rc.env.get_role("PM").cur_doc_name #获取当前pm需求需要写入的文档内容
        msg = await todo.run(doc_name, self.get_memories(k=1)[0].content)

        msg = Message(content=msg, role=self.profile,
                      cause_by=type(todo))
        #广播数据已经写入完成
        #self.publish_message(msg)
        # logger.info(f"下一次处理的文件内容为:{msg}")
        return msg

