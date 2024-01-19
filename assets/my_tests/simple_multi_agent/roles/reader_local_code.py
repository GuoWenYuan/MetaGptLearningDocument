import asyncio
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from my_tests.simple_multi_agent.actions import LocalCoderReader

class ReaderLocalCode(Role):
    name: str = "ReaderLocalCode"
    profile: str = "LocalCodeReader"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化 本地代码读取
        # 突然思考到 action的运行顺序可以按照顺序执行，也可以根据llm来进行动态规划 -> 使用固定格式让llm返回调用的action index即可
        self.init_actions([LocalCoderReader])
        self._set_react_mode("by_order")


    async def _act(self) -> Message:
        """这里重写_act的逻辑原因是我们在当前步骤不需要与大模型产生交互"""
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo #todo = 读取本地代码文件

        msg = self.get_memories(k=2)[0]  # find the most recent messages
        running_resp = await todo.run(msg.content)
        msg = Message(content=running_resp, role=self.profile,
                      cause_by=type(todo))
        self.rc.memory.add(msg)  #为角色增加记忆,记忆内容为本地读取文件的json内容

        return msg


#asyncio.run(ReaderLocalCode().run("C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py;C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/roles/role.py"))