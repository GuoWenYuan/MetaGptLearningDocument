from metagpt.team import Team
from my_tests.simple_multi_agent.roles import DocReviewRole,ReaderLocalCode,DocCreatorRole,WriteDocRole
import asyncio

company = Team()
company.hire(
    [
        ReaderLocalCode(),
        DocReviewRole(),
        DocCreatorRole(),
        WriteDocRole()
    ]
)

company.run_project("C:/Users/GuoWY/Desktop/MetaGPT-main/metagpt/actions/action.py")
asyncio.run(company.run())
