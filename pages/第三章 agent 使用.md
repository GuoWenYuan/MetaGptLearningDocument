- 官方教程地址: https://deepwisdom.feishu.cn/docx/RJmTdvZuPozAxFxEpFxcbiPwnQf
- 这里对于agent的使用，单智能体的编写与应用仿照官方例子去测试即可，上一章节已经讨论过agent是什么以及如何使用了。
  collapsed:: true
	- *需要注意，教程应该使用的是metagpt0.4版本，最新版本0.6的版本中有很多命名与生成方式被修改，在新版本中可使用以下代码尝试*
	- ```
	  import re
	  import asyncio
	  from metagpt.actions import Action
	  from metagpt.roles import Role
	  from metagpt.schema import Message
	  from metagpt.logs import logger
	  
	  class SimpleWriteCode(Action):
	      PROMPT_TEMPLATE: str = """
	      Write a python function that can {instruction} and provide two runnnable test cases.
	      Return ```python your_code_here ``` with NO other texts,
	      your code:
	      """
	      name: str = "SimpleWriteCode"
	  
	      async def run(self, instruction: str):
	          prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
	  
	          rsp = await self._aask(prompt)
	          print(rsp)
	          code_text = SimpleWriteCode.parse_code(rsp)
	  
	          return code_text
	  
	      @staticmethod
	      def parse_code(rsp):
	          pattern = r'```csharp(.*)```'
	          match = re.search(pattern, rsp, re.DOTALL)
	          code_text = match.group(1) if match else rsp
	          return code_text
	  
	  class SimpleCoder(Role):
	      def __init__(
	          self,
	          name: str = "Alice",
	          profile: str = "SimpleCoder",
	          **kwargs,
	      ):
	          super().__init__(**kwargs)
	          self.name = name
	          self.profile = profile
	          self._init_actions([SimpleWriteCode])
	  
	      async def _act(self) -> Message:
	          logger.info(f" ready to {self.rc.todo}")
	          todo = self.rc.todo  # *todo will be SimpleWriteCode()
	  
	          msg = self.get_memories(k=1)[0]  # find the most recent messages
	  
	          code_text = await todo.run(msg.content)
	          msg = Message(content=code_text, role=self.profile,
	                        cause_by=type(todo))
	  
	          return msg
	  
	  print(asyncio.run(SimpleCoder().run("使用python写一个快速排序方法,并写出对应的测试用例")))
	  ```
-
- 那么在官方多智能体的例子中，我做了一定修改，对于我自身来说，对python不是很熟悉，源码中掺杂了大量的语法糖与第三方的python库，对于不熟悉的内容，我每次都需要一个个去查，所以我决定将多智能体的例子修改为: **使用多agent的配合来完成理解metagpt代码,并将其中大量的python语法糖与第三方库的用法及相关内容保存到本地(现有的code相关ai工具也能完成，但是我依然嫌每次打开和交流很麻烦，而且有时候可能我会遗忘掉他介绍过的内容)**
- 第一步:拆分需求:
	- 1.实际需求: `找到想理解的代码 -> 阅读代码,并翻译代码->找到代码里的第三方库与语法糖-> 整理成md文档 -> 收到教程 -> 写入本地需要阅读的代码可能有很多个文件，所以在实际需求中的步骤会反复执行多轮，不一起请求也是担心token超过最大数量限制，所以我们在Role中加入了一个新的角色，称之为审核的角色，主要职能是审核是否完成了用户所有对于代码阅读的需求。
	- 2.拆分需要使用到的Role: `读取代码角色->确定所有内容是否已经写入完成->理解代码角色->编写教程内容角色->在本地写入文件角色`
	- 3.拆分需要使用到的Action:  `读取本地代码行为->确定内容是否写入完成行为->编写教程内容行为->在本地写文件行为`
	- 为方便理解，我们画一张小图来更加形象的表述一下这个流程
	- https://github.com/GuoWenYuan/MetaGptLearningDocument/blob/main/assets/%E6%BA%90%E7%A0%81%E7%B2%BE%E8%AF%BB%E5%B7%A5%E5%85%B7.png?raw=true
- 第二步:相关Action的编写:
	- 1.读取本地代码的->`LocalCoderReader`  相关实现代码如下(当然给文件夹路径也可以，稍微修改下就行了)
	- ```
	  from metagpt.actions import Action
	  import json
	  from metagpt.logs import logger
	  import asyncio
	  
	  
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
	  
	  ```
	- 2.审核是否完成了所有code内容的Action -> `DocReviewAction` ,这里只是进行了简单的返回占位，用于其他模块来监听该行为，实际上的工作内容是由PM角色来进行分发，当然这里也可以进一步修改为由LLM来决定当前写的MD文档是否合格。相关代码如下
	- ```
	  from metagpt.actions import Action
	  
	  
	  class DocReviewAction(Action):
	      """PM通知其他模块进行处理 ~"""
	  
	      name: str = "CoderToolContentReview"
	      create_doc_success: bool = False
	  
	      async def run(self, instruction: str):
	          """获取instruction"""
	          return instruction
	  
	  
	  
	  
	  
	  
	  ```
	- 3.编写MD文档内容的Action->`DocCreatorAction`,这里不需要太多处理，只需要返回大模型的处理结果即可，代码如下：
	- ```
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
	          """**获取**instruction"""
	          return await self._aask(self.prompt.replace('{instruction}', instruction))
	  ```
	- 4.写入本地文件的Action->`WriteDocAction` , 这个角色多了一个参数为文件名称，将由其Role获取后传给这个行为，来决定写入本地的文件名称，同时，为了方便，我们定义了一个公用路径`path`来觉得最终写入的路径，**path.py**代码如下：
	- ```
	  import os
	  from os import path
	  - DocPath = "CodeDoc"
	  - def get_doc_path()->str:
	    real_path = os.getcwd() + '/' + DocPath
	    if not path.exists(real_path):
	        #如果不存在则创建目录（包含父目录）
	        os.makedirs(real_path)
	    return real_path
	  - DocName = ''
	  ```
	- **WriteDocAction**代码如下：
	- ```
	  from metagpt.actions import Action
	  from metagpt.logs import logger
	  import os
	  import re
	  from my_tests.simple_multi_agent.path import get_doc_path
	  
	  class WriteDocAction(Action):
	  
	      name: str = "WriteDocAction"
	  
	      async def run(self, file_name: str, instruction: str):
	          *"""instruction=**大模型返回的结果**  file_name=**要写入的文件名称**"""
	  *        real_path = f'{get_doc_path()}/{file_name}'
	  
	          with open(real_path, 'w', encoding='utf-8') as f:
	              f.write(self._convert_markdown(instruction))
	          logger.info(f"success write {file_name}")
	          return f"success write {file_name}"
	  
	      def _convert_markdown(self, msg):
	          *"""**匹配**markdown**文件 返回格式为**'''markdown''' xxxxx"""
	  *        pattern = r'```markdown(.*)```'
	          match = re.search(pattern, msg, re.DOTALL)
	          code_text = match.group(1) if match else msg
	          return code_text
	  ```
- 第三步：相关Role的编写:
  collapsed:: true
	- 1. 读取本地文件Role->`ReaderLocalCode`,其在获取用户指令后，将对应指令放入其Action中进行处理，相关代码如下：
	- ```
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
	          """**这里重写**_act**的逻辑原因是我们在当前步骤不需要与大模型产生交互**"""
	          logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
	          todo = self.rc.todo #*todo = **读取本地代码文件
	  
	          msg = self.get_memories(k=2)[0]  # find the most recent messages
	          running_resp = await todo.run(msg.content)
	          msg = Message(content=running_resp, role=self.profile,
	                        cause_by=type(todo))
	          self.rc.memory.add(msg)  #为角色增加记忆,记忆内容为本地读取文件的json内容
	  
	          return msg
	  
	  #测试
	  #asyncio.run(ReaderLocalCode().run("C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py;C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/roles/role.py"))
	  ```
	- 2.决定流程的Role->`PMRole`  该角色监听了两个行为，一个是本地代码读取行为，一个是本地代码写入完成行为，在本地代码读取行为完成后来进行任务拆分，并进行自己对应行为的处理。在本地代码写入完成后判断所有流程是否已经结束，未结束继续通过Action进行下一个任务的分发。代码如下：
	- ```
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
	      *"""code**数据类**"""
	  *    file_name: str = ''
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
	          *"""**我们这里拿到角色**reader_local_code**的最后一条记忆**"""
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
	          *"""**获取下一个要处理的代码文档**"""
	          if len(self.code_contents) == 0:
	              return None
	          code_data = self.code_contents.pop()
	          self.cur_doc_name = code_data.doc_name
	          return code_data
	  
	      def _convert_code_msg(self,msg):
	          *"""**将本地代码的**msg**转换为文档的**msg"""
	          data = json.loads(msg)
	          for doc_data in data:
	              # print(f'我的data：{doc_data}')
	              doc_data = json.loads(doc_data)  # 转换一下json
	              doc_name = doc_data.get('code_name')
	              doc_data['code_name'] = doc_name.split('.')[0] + '.md'
	              self.code_contents.append(CodeData(file_name=doc_name,doc_name=doc_data['code_name'],code_content=doc_data['code_content']))
	  ```
	- 3.创建文档角色->`DocCreatorRole`,该角色监听了PM角色的`DocReviewAction`行为，该行为会发放当前需要生成文档的代码具体内容。具体代码如下：
	- ```
	  from metagpt.roles import Role
	  from metagpt.schema import Message
	  from metagpt.logs import logger
	  from my_tests.simple_multi_agent.actions import DocReviewAction,DocCreatorAction
	  
	  class DocCreatorRole(Role):
	      """**创建文档的角色**"""
	  
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
	          self._watch([DocReviewAction]) #监听PM的行为
	  
	      async def _act(self) -> Message:
	          todo = self.rc.todo
	          #写入角色
	          todo.set_prefix(self.prompt)
	          instruction = self.get_memories(k=1)[0].content
	          msg = await todo.run(instruction) #获取最近一条记忆，该记忆会从env publish_message 时放入
	          return Message(content=msg, role=self.profile, cause_by=type(todo))
	  ```
	- 4.写入本地文件的角色->`WriteDocRole`,该角色会监听文档创建的行为，当文档创建行为结束后，会根据生成结果，从PM角色中拿到具体当前的文档名称，调用该行为的写入功能来写入大模型生成的文档内容。相关代码如下：
	- ```
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
	        return msg
	  ```
- 第四步：组合后进行运行,相关代码(可将run中的路径换成你需要他读取文件的路径)：
	- ```
	  from metagpt.team import Team
	  from my_tests.simple_multi_agent.roles import PMRole,ReaderLocalCode,DocCreatorRole,WriteDocRole
	  import asyncio
	  - company = Team()
	  company.hire(
	    [
	        ReaderLocalCode(),
	        PMRole(),
	        DocCreatorRole(),
	        WriteDocRole()
	    ]
	  )
	  #"C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/team.py"
	  company.run_project('C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/design_api.py;'
	                    'C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/project_management.py')#"C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py;C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/roles/role.py")
	  asyncio.run(company.run(n_round=10))
	  ```
	- 这里的n_round 运行次数为10次，因metagpt运行方式为并行执行所有的Role，若Role中有新的记忆则进行执行，不然不运行，这里新的记忆来源于该角色监听的行为。当前运行结束后，未被运行到的内容将不会再运行，等待下次运行后重新检索记忆中是否有记忆才会进行运行。当然可以使用在role内部循环的逻辑来执行多次行为，但个人觉得这样的方式不太智能，退出执行逻辑应该只有两个，一是资金不足，二是任务完成，不应该由n_round来控制执行次数以保证能完成任务。
	- 最终生成的相关文档会在代码同目录的CodeDoc生成。
- 内容总结：
	- 通过上面的例子，我们基本理清楚了metagpt的运行流程，单次运行流程见下图:
	- https://github.com/GuoWenYuan/MetaGptLearningDocument/blob/main/assets/metagpt%E8%BF%90%E8%A1%8C%E6%B5%81%E7%A8%8B.jpg?raw=true
	- 而n_round 控制的是执行这个逻辑执行多少次
	- 我们结合Agent的定义来理解一下这些模块,见下图:
	- https://github.com/GuoWenYuan/MetaGptLearningDocument/blob/main/assets/Agent%E4%B8%8EMetagpt.jpg?raw=true
-
-
-