from metagpt.roles import Role
from metagpt.schema import Message
from my_tests.simple_multi_agent.actions import DocReviewAction,LocalCoderReader,WriteDocAction
from metagpt.logs import logger

class DocReviewRole(Role):
    name: str = "DocReviewRole"
    profile: str = "DocReviewRole"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_actions([DocReviewAction])
        self._set_react_mode("by_order")
        self._watch([LocalCoderReader,WriteDocAction])

    async def _act(self) -> Message:
        """我们这里拿到角色reader_local_code的最后一条记忆"""
        self._set_state(0)
        rc = self.rc.env.get_role("LocalCodeReader")
        todo = self.rc.todo
        #logger.info(rc.get_memories(k=1)[0])
        msg = await todo.run(rc.get_memories(k=1)[0].content)

        msg = Message(content=msg, role=self.profile,
                      cause_by=type(todo))
        if not todo.create_doc_success:
            self.publish_message(msg)
        #logger.info(f"下一次处理的文件内容为:{msg}")
        return msg
