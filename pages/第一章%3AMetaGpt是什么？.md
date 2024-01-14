- MetaGpt git地址:https://github.com/geekan/MetaGPT
- MetaGpt能做什么(以下均仅代表个人浅薄观点)？
	- 这里我们引用MetaGpt 文档中的一句话来总结与引申
	- `Code = SOP(Team)` is the core philosophy. We materialize SOP and apply it to teams composed of LLMs.
	- `Code = SOP(Team)` is the core philosophy. 这前半句话总结了metagpt的核心理念，即SOP(Team)
		- 首先SOP 是什么，定义是[标准作业程序] ,即可被标准化的工作/学习流程
		- 把大象塞进冰箱里需要几步，拆分出来的工作内容就是SOP
		- 那么metagpt所有的设计均是基于该理念进行制作的.
		- 我们来引用下同样是该文档中的示意图，该图表示了一个软件公司真实的SOP在MetaGpt中是如何实现的。
		- https://docs.deepwisdom.ai/main/assets/software_company_cd.7154a15c.jpg
		- 从左至右就是MetaGpt的工作流程-Boss(提出要求,这里的Boss指的就是每一个开发者)->Product(拆分需求)->Architect(设计架构)->Project(项管拆分任务)->Engineer(写代码)->QA(测试)
		- 在这个过程中，我们注意到有大量Review ，这是非常符合一个软件公司的SOP的，这样来确保生成出的内容更加的接近我们想要的产品的内容。
		- 当然，实际中可能在Engineer或者QA，甚至QA后阶段Boss还会有新的Revise要求，或者在过程中也会有，来自其他人员的Review要求/新的Requirement，针对这部分，MetaGpt也做了相应的内容，后面的章节中应该会补充(即人为干预)
	- We materialize SOP and apply it to teams composed of LLMs.后半句话总结了自动化的实现方式
		- 即使用LLM 大模型来进行每一个步骤的自动化
		- 这句话比较好理解，就是使用LLM大模型来完成SOP中的每一个环节
	- 那么我们重新来理解这句话就是，使用大模型来完成制定的标准化流程，最终完成Boss(指代我们自己)的要求。
	-
- MetaGpt部署流程:
	- 1.在你的代码编辑器终端中使用 git clone https://github.com/geekan/MetaGPT
		- 这里笔者clone的是最新的0.6版本，这里仅是个人习惯，因为在metaGpt不断升级的过程中，大量的好的结构与思想不对的完善以及修改，而且如果在运行因版本过新导致的bug也可以使我们在debug的过程中更加了解metagpt的实现流程
			-
	- 2.环境初始化
		- 在编辑器终端输入`pip install -r .\requirements.txt`即可快速收集相关引用
	- 3.配置文件:
		- 配置文件路径：MetaGpt/config/config.yaml
		- 可复制一份config.yaml,并重命名为key.yaml，在文件中进行相关LLM的配置即可
		- 当然直接在config.yaml中进行修改也可，但是要注意在commit 过程中不要提交你的大模型的配置
		- 最新版本中的模型默认是openai，若想修改为其他默认大模型可在配置文件中修改*DEFAULT_PROVIDER* 字段为你需要的基础模型，具体对应的枚举类型在MetaGpt/metagpt/config.py中
	- 4.运行第一行代码:
		- 在MetaGpt目录下新建代码test1
		- 内容如下
		- ```
		  import asyncio
		  from metagpt.roles import (
		    Architect,
		    Engineer,
		    ProductManager,
		    ProjectManager,
		  )
		  from metagpt.team import Team
		  - async def startup(idea: str):
		    company = Team()
		    company.hire(
		        [
		            ProductManager(),
		            Architect(),
		            ProjectManager(),
		            Engineer(),
		        ]
		    )
		    company.invest(investment=3.0)
		    company.run_project(idea=idea)
		  - await company.run(n_round=5)
		  - asyncio.run(startup("写一个2048的网页游戏，除代码外使用中文"))
		  ```
	- 运行该代码即可(笔者这里仅是为了debug方便，若你使用metagpt中的startup方式来进行第一个测试，则不需要收集依赖于增加test1类，仅需进入metagpt目录在终端执行**python startup.py --idea "write a cli blackjack game"**即可)
-