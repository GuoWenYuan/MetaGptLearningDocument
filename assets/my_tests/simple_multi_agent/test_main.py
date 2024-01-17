from metagpt.team import Team
from my_tests.simple_multi_agent.roles import CoderToolReviewRole,ReaderLocalCode
import asyncio

company = Team()
company.hire(
    [
        ReaderLocalCode(),
        CoderToolReviewRole()
    ]
)

company.run_project("C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py;C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/roles/role.py")
asyncio.run(company.run())
