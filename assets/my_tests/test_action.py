from metagpt.team import Team
from my_tests.simple_multi_agent.roles import PMRole,ReaderLocalCode,DocCreatorRole,WriteDocRole
import asyncio

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
company.run_project('C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/design_api.py;'
                    'C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/project_management.py')#"C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py;C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/roles/role.py")
asyncio.run(company.run(n_round=10))
