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
	- 1.实际需求: `找到想理解的代码 -> 阅读代码,并翻译代码->找到代码里的第三方库与语法糖-> 整理成md文档 -> 收到教程 -> 写入本地`
	- 2.拆分需要使用到的Role: `理解代码的->编写教程内容的->在本地写入文件的`
	- 3.拆分需要使用到的Action:  `读取本地代码的->理解代码的->理解第三方库和语法糖的->编写教程内容的->在本地写文件的`
	- 4.这里有一个问题，即需要阅读的代码可能有很多个文件，所以在实际需求中的步骤会反复执行多轮，不一起请求也是担心token超过最大数量限制，所以我们在Role中加入了一个新的角色，称之为审核的角色，主要职能是审核是否完成了用户所有对于代码阅读的需求。
	- 5.最终我希望他能根据每一个代码文件输出一个md文件，内容是单个代码文件的具体讲解，包括源码解读，第三方库的讲解与例子，相关用到语法糖的介绍
	- 为方便理解，我们画一张小图来更加形象的表述一下这个流程
	- ![源码精读工具.png](../assets/源码精读工具.png)
- 第二步:相关Action的编写:
	- 1.读取本地代码的->`LocalCoderReader`  相关实现代码如下(当然给文件夹路径也可以，稍微修改下就行了，我这里是测试阶段想省一些token)
	- ```
	  from metagpt.actions import Action
	  import json
	  from metagpt.logs import logger
	  import asyncio
	  
	  #官方教程地址:https://deepwisdom.feishu.cn/docx/RJmTdvZuPozAxFxEpFxcbiPwnQf
	  #我们尝试使用多agent的配合来完成理解metagpt代码中大量的python语法糖与第三方库的用法，由于对python不太熟悉，每次都要看语法糖与第三方库相关的东西太麻烦了，所以改下官方教程里的例子，变成我能用到的
	  
	  class LocalCoderReader(Action):
	      *"""**获取本地的代码** ~
	  **
	  **       Args:
	  *           *用于读取本地代码。
	  **           参数：**
	  **           name**：**LocalCoderReader**。**
	  **           language**：输出的语言，默认为**"Chinese"**。
	  **       这里并不需要他和**llm**产生直接交互，我们自己来读取代码内容即可**
	  **    """
	  **
	      name: str = "LocalCoderReader"
	  
	      async def run(self, instruction: str):
	          *"""instruction=**本地需要理解代码的路径，为了方便我们定义格式，以**;**号来切分不同的路径（当然也可以用**json**，我只是单纯的懒）**"""
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
	          return resp
	  
	      def split_path(code_paths:str):
	          *"""**按照**;**号切分路径**"""
	          if ';' in code_paths:
	              return code_paths.split(";")
	          return [code_paths]
	  
	  #测试例子
	  #asyncio.run(LocalCoderReader().run("your code path1;your code path2"))
	  ```
	- 2.审核是否完成了所有code内容的Action -> `CoderToolContentReview` 相关代码如下
	-
-