class SkillRegistry:
    def __init__(self):
        self._skills = {"wallet_manager", "trend_hunter", "image_generator"}

    def is_known(self, skill: str) -> bool:
        return skill in self._skills

    def get_queue(self, skill: str) -> str:
        if not self.is_known(skill):
            raise KeyError("unknown skill")
        return skill
