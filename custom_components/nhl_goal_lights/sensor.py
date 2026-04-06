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

# Example team color mapping for WLED
TEAM_COLORS = {
    "BOS": [255, 200, 0],
    "NYR": [0, 0, 255],
    "TOR": [0, 32, 91],
    "CHI": [206, 17, 38],
    # Add all NHL teams here...
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up NHL Goal Lights sensor platform."""
    sensor = NHLGameSensor(hass, entry)
    async_add_entities([sensor], True)
    hass.loop.create_task(sensor.periodic_update())


class NHLGameSensor(Entity):
    """Sensor to track NHL goals and trigger WLED."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self._hass = hass
        self._entry = entry
        self._state = None
        self._attr_name = "NHL Game Sensor"
        self._last_scores = {}  # track previous scores

        # User configuration
        self.monitor_teams = entry.data.get("monitor_teams", [])
        self.all_games = entry.data.get("all_games", True)
        self.wled_devices = entry.data.get("wled_devices", [])

    @property
    def state(self):
        return self._state

    async def periodic_update(self):
        """Periodically poll NHL API."""
        while True:
            try:
                await self.async_update()
            except Exception as e:
                _LOGGER.error("Error updating NHL sensor: %s", e)
            await asyncio.sleep(60)  # poll every 60s

    async def async_update(self):
        """Fetch NHL scoreboard and detect goals."""
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

                # Only monitor selected teams
                if self.all_games or home_team in self.monitor_teams or away_team in self.monitor_teams:
                    new_scores[game["gamePk"]] = {"home": home_score, "away": away_score}

                    # Goal detection
                    if game["gamePk"] in self._last_scores:
                        old_home = self._last_scores[game["gamePk"]]["home"]
                        old_away = self._last_scores[game["gamePk"]]["away"]

                        if home_score > old_home:
                            _LOGGER.info(f"Goal scored by {home_team}!")
                            await self.trigger_wled(home_team)

                        if away_score > old_away:
                            _LOGGER.info(f"Goal scored by {away_team}!")
                            await self.trigger_wled(away_team)

        self._last_scores = new_scores
        self._state = new_scores or "No games"

    async def trigger_wled(self, team_name):
        """Send goal effect to WLED devices."""
        color = TEAM_COLORS.get(team_name[:3], [255, 255, 255])  # fallback white

        for device_ip in self.wled_devices:
            url = f"http://{device_ip}/json/state"
            payload = {
                "on": True,
                "seg": [{"col": [color]}],
                "fx": 62  # example effect, you can choose different WLED effects
            }
            try:
                requests.post(url, json=payload, timeout=2)
                _LOGGER.info(f"WLED triggered for {team_name} on {device_ip}")
            except Exception as e:
                _LOGGER.error(f"WLED error for {device_ip}: {e}")
