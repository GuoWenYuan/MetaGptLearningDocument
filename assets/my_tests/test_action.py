from metagpt.team import Team
from my_tests.simple_multi_agent.roles import PMRole,ReaderLocalCode,DocCreatorRole,WriteDocRole
import asyncio
from my_tests.QA_Agent.Actions.game_design import ActionGameDesign

"""
company = Team()
company.hire(
    [
        ReaderLocalCode(),
        PMRole(),
        DocCreatorRole(),
        WriteDocRole()
    ]
)
 #"C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/team.py"
#company.run_project('C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/design_api.py;'
#                    'C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/project_management.py')#"C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py;C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/roles/role.py")
#asyncio.run(company.run(n_round=10))
"""

asyncio.run(ActionGameDesign().run("C:/Game/PC_Creative/X_系统/01简版魔域参考内容/交易系统/陌生人间限制高价值物品及魔石交易.docx"))