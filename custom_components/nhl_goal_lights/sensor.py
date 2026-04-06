from homeassistant.helpers.entity import Entity
from .const import DOMAIN

class NHLGameSensor(Entity):
    def __init__(self, hass, config):
        self.hass = hass
        self._state = None
        self._attr = {}

    @property
    def name(self):
        return "NHL Game Sensor"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attr

    async def async_update(self):
        # Fetch live NHL data via API (pseudo code)
        # Example:
        # data = await fetch_nhl_scores()
        data = {
            "home_team": "TOR",
            "away_team": "MTL",
            "home": 3,
            "away": 2,
            "period": 3,
            "time_remaining": "05:32",
            "shots": {"home": 28, "away": 26},
            "power_play": {"home": False, "away": True}
        }
        self._state = f"{data['home']} - {data['away']}"
        self._attr = data
