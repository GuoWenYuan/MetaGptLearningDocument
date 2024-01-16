import asyncio
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from my_tests.simple_multi_agent import CoderToolContentReview, LocalCoderReader

class CoderContentReview(Role):
    name: str = "CoderContentReview"
    profile: str = "检测所有文件的文档是否已经生成完毕"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化 本地代码读取与 代码精度审查工具  这里action 按顺序执行
        # 突然思考到 action的运行顺序可以按照顺序执行，也可以根据llm来进行动态规划 -> 使用固定格式让llm返回调用的action index即可
        self.init_actions([LocalCoderReader, CoderToolContentReview])
        logger.info("action 初始化完成")


    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()

        msg = self.get_memories(k=1)[0]  # find the most recent messages
        running_resp = await todo.run(msg.content)
        msg = Message(content=running_resp, role=self.profile,
                      cause_by=type(todo))
        self.rc.memory.add(msg)  #为角色增加记忆
        #self.publish_message(msg)
        return msg

    async def _react(self) -> Message:
        """角色默认的react_mode == RoleReactMode.REACT  这里重写_react即可"""
        self._set_state(0)
        rsp = await self._act()
        self._set_state(1)
        return await self._act()




asyncio.run(CoderContentReview().run("C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py;C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/roles/role.py"))