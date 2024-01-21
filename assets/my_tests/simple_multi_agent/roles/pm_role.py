from metagpt.roles import Role
from metagpt.schema import Message
from my_tests.simple_multi_agent.actions import DocReviewAction,LocalCoderReader,WriteDocAction
from metagpt.logs import logger
import json
from metagpt.utils.common import (
    any_to_name,
)
from pydantic import BaseModel, SkipValidation


class CodeData(BaseModel):
    """code数据类"""
    file_name: str = ''
    code_content: str = ''
    doc_name: str = ''


class PMRole(Role):
    name: str = "PM"
    profile: str = "PM"
    code_contents: list[SkipValidation[CodeData]] = []
    cur_doc_name:  str = '' #当前处理的文档名称

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_actions([DocReviewAction])
        self._set_react_mode("by_order")
        self._watch([LocalCoderReader,WriteDocAction])

    async def _act(self) -> Message:
        """我们这里拿到角色reader_local_code的最后一条记忆"""
        self._set_state(0)
        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]

        #如果是本地代码内容已经读取完成，记录并进行下一步骤
        if any_to_name(LocalCoderReader) in msg.cause_by:
            content = msg.content
            self._convert_code_msg(content)

        #获取下一阶段要处理的代码文档
        next_create_doc = self._get_next_create_doc()

        if next_create_doc is None:
            logger.info("所有数据处理完成")
            return Message(content='处理完成', role=self.profile, cause_by='处理结束')

        logger.info(f"下一个要处理的数据为:{next_create_doc}")
        msg = await todo.run(next_create_doc.code_content)

        msg = Message(content=msg, role=self.profile,
                      cause_by=type(todo))
        self.rc.memory.add(msg) #这里其实加不加都行
        return msg



    def _get_next_create_doc(self):
        """获取下一个要处理的代码文档"""
        if len(self.code_contents) == 0:
            return None
        code_data = self.code_contents.pop()
        self.cur_doc_name = code_data.doc_name
        return code_data

    def _convert_code_msg(self,msg):
        """将本地代码的msg转换为文档的msg"""
        data = json.loads(msg)
        for doc_data in data:
            # print(f'我的data：{doc_data}')
            doc_data = json.loads(doc_data)  # 转换一下json
            doc_name = doc_data.get('code_name')
            doc_data['code_name'] = doc_name.split('.')[0] + '.md'
            self.code_contents.append(CodeData(file_name=doc_name,doc_name=doc_data['code_name'],code_content=doc_data['code_content']))
