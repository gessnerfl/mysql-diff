class Diff:
    def __init__(self, asset_name: str, asset_type: str, diff: str):
        self.asset_name = asset_name
        self.asset_type = asset_type
        self.diff = diff


class DatabaseDiffs:
    def __init__(self):
        self.diffs = []

    def append_diff(self, diff: Diff):
        self.diffs.append(diff)
