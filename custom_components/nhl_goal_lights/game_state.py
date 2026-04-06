class GameState:
    def __init__(self):
        self.previous = {}
        self.player_goals = {}

    def update(self, games):
        events = []

        for g in games:
            gid = g["id"]

            prev = self.previous.get(gid, {})
            curr = {
                "home": g["homeTeam"]["score"],
                "away": g["awayTeam"]["score"],
            }

            if prev:
                if curr["home"] > prev["home"]:
                    events.append(self._goal_event(g, "home"))
                if curr["away"] > prev["away"]:
                    events.append(self._goal_event(g, "away"))

            self.previous[gid] = curr

        return events

    def _goal_event(self, g, side):
        team = g["homeTeam"]["abbrev"] if side == "home" else g["awayTeam"]["abbrev"]

        scorer = g.get("lastGoal", {}).get("scorer", "unknown")
        key = f"{g['id']}:{scorer}"

        self.player_goals[key] = self.player_goals.get(key, 0) + 1

        event = {"type": "goal", "team": team}

        if self.player_goals[key] == 3:
            event["type"] = "hat_trick"
            event["player"] = scorer

        return event