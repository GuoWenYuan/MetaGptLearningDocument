from metagpt.actions import Action


class DocReviewAction(Action):
    """PM通知其他模块进行处理 ~"""

    name: str = "CoderToolContentReview"
    create_doc_success: bool = False

    async def run(self, instruction: str):
        """获取instruction"""
        return instruction





