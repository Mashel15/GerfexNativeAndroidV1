class BrainManager:
    def __init__(self):
        self.primary_brain = "Queen"
        self.owner = "Gerfex"
        self.rule = (
            "Queen is the core brain. "
            "External models are helper tools only."
        )

    def decide(self, context):
        return {
            "brain": self.primary_brain,
            "owner": self.owner,
            "rule": self.rule,
            "context": context,
            "decision": "queen_first"
        }
