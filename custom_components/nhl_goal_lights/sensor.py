import logging
import asyncio
import requests
from datetime import datetime

from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

NHL_API_SCOREBOARD = "https://statsapi.web.nhl.com/api/v1/schedule"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up NHL Goal Lights sensor platform."""
    sensor = NHLGameSensor(hass, entry)
    async_add_entities([sensor], True)
    # Schedule periodic updates
    hass.loop.create_task(sensor.periodic_update())

class NHLGameSensor(Entity):
    """Sensor to track NHL goals and game state."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self._hass = hass
        self._entry = entry
        self._state = None
        self._attr_name = "NHL Game Sensor"
        self._last_scores = {}  # track previous scores to detect goals

        # User config
        self.monitor_teams = entry.data.get("monitor_teams", [])
        self.all_games = entry.data.get("all_games", True)
        self.wled_devices = entry.data.get("wled_devices", [])

    @property
    def state(self):
        return self._state

    async def periodic_update(self):
        """Periodically update NHL game state."""
        while True:
            try:
                await self.async_update()
            except Exception as e:
                _LOGGER.error("Error updating NHL sensor: %s", e)
            await asyncio.sleep(60)  # poll every 60s

    async def async_update(self):
        """Fetch NHL data and detect goals."""
        today = datetime.now().strftime("%Y-%m-%d")
        params = {"date": today}
        response = requests.get(NHL_API_SCOREBOARD, params=params)
        data = response.json()

        new_scores = {}

        for date_info in data.get("dates", []):
            for game in date_info.get("games", []):
                home = game["teams"]["home"]["team"]["name"]
                away = game["teams"]["away"]["team"]["name"]
                home_score = game["teams"]["home"]["score"]
                away_score = game["teams"]["away"]["score"]

                # Filter teams if user selected specific teams
                if self.all_games or home in self.monitor_teams or away in self.monitor_teams:
                    new_scores[game["gamePk"]] = {"home": home_score, "away": away_score}

                    # Detect goals
                    if game["gamePk"] in self._last_scores:
                        old_home = self._last_scores[game["gamePk"]]["home"]
                        old_away = self._last_scores[game["gamePk"]]["away"]

                        if home_score > old_home:
                            _LOGGER.info(f"Goal scored by {home}!")
                            await self.trigger_wled(home)

                        if away_score > old_away:
                            _LOGGER.info(f"Goal scored by {away}!")
                            await self.trigger_wled(away)

        self._last_scores = new_scores
        self._state = new_scores or "No games"

    async def trigger_wled(self, team_name):
        """Trigger WLED lights for a goal. Placeholder."""
        _LOGGER.info(f"Triggering WLED for {team_name} on devices: {self.wled_devices}")
        # Here you can implement actual WLED API calls:
        # Example: send JSON to http://<wled-ip>/json to change color/effect
