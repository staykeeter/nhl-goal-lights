import logging
import asyncio
import requests
from datetime import datetime

from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, TEAM_COLORS, NHL_TEAMS

_LOGGER = logging.getLogger(__name__)
NHL_API_SCOREBOARD = "https://statsapi.web.nhl.com/api/v1/schedule"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    sensor = NHLGameSensor(hass, entry)
    async_add_entities([sensor], True)
    hass.loop.create_task(sensor.periodic_update())

class NHLGameSensor(Entity):
    """Sensor to track NHL goals and WLED lighting."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self._hass = hass
        self._entry = entry
        self._state = None
        self._attr_name = "NHL Game Sensor"
        self._last_scores = {}

        self.monitor_teams = entry.data.get("monitor_teams", [])
        self.all_games = entry.data.get("all_games", True)
        self.wled_devices = entry.data.get("wled_devices", [])

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        attrs = {}
        for game_pk, info in (self._state or {}).items():
            attrs[game_pk] = {
                "home_team": info.get("home_team"),
                "away_team": info.get("away_team"),
                "home_score": info.get("home"),
                "away_score": info.get("away"),
                "period": info.get("period"),
                "time_remaining": info.get("time_remaining"),
                "shots_on_goal": info.get("shots"),
                "power_play": info.get("power_play")
            }
        return attrs

    async def periodic_update(self):
        while True:
            try:
                await self.async_update()
            except Exception as e:
                _LOGGER.error("Error updating NHL sensor: %s", e)
            await asyncio.sleep(60)

    async def async_update(self):
        today = datetime.now().strftime("%Y-%m-%d")
        params = {"date": today}
        response = requests.get(NHL_API_SCOREBOARD, params=params, timeout=5)
        data = response.json()
        new_scores = {}

        for date_info in data.get("dates", []):
            for game in date_info.get("games", []):
                home_team = game["teams"]["home"]["team"]["name"]
                away_team = game["teams"]["away"]["team"]["name"]
                home_score = game["teams"]["home"]["score"]
                away_score = game["teams"]["away"]["score"]

                if self.all_games or home_team in self.monitor_teams or away_team in self.monitor_teams:
                    new_scores[game["gamePk"]] = {
                        "home_team": home_team,
                        "away_team": away_team,
                        "home": home_score,
                        "away": away_score,
                        "period": game.get("linescore", {}).get("currentPeriod", 1),
                        "time_remaining": game.get("linescore", {}).get("currentPeriodTimeRemaining", "20:00"),
                        "shots": {
                            "home": game.get("linescore", {}).get("teams", {}).get("home", {}).get("shotsOnGoal", 0),
                            "away": game.get("linescore", {}).get("teams", {}).get("away", {}).get("shotsOnGoal", 0)
                        },
                        "power_play": {
                            "home": game.get("linescore", {}).get("teams", {}).get("home", {}).get("powerPlayInfo", {}),
                            "away": game.get("linescore", {}).get("teams", {}).get("away", {}).get("powerPlayInfo", {})
                        }
                    }

                    if game["gamePk"] in self._last_scores:
                        old = self._last_scores[game["gamePk"]]
                        if home_score > old.get("home", 0):
                            _LOGGER.info(f"Goal scored by {home_team}!")
                            await self.trigger_wled(home_team)
                        if away_score > old.get("away", 0):
                            _LOGGER.info(f"Goal scored by {away_team}!")
                            await self.trigger_wled(away_team)

        self._last_scores = new_scores
        self._state = new_scores or "No games"

    async def trigger_wled(self, team_name):
        color = TEAM_COLORS.get(team_name[:3], [255, 255, 255])
        for device in self.wled_devices:
            payload = {"on": True, "seg": [{"col": [color], "fx": 62}]}
            try:
                requests.post(f"http://{device}/json/state", json=payload, timeout=2)
                _LOGGER.info(f"WLED triggered for {team_name} on {device}")
            except Exception as e:
                _LOGGER.error(f"WLED error for {device}: {e}")
