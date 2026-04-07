from homeassistant.helpers.entity import Entity
from .config_flow import NHL_TEAMS

DOMAIN = "nhl_goal_lights"

class NHLGameSensor(Entity):
    def __init__(self, hass, name, game_id):
        self._hass = hass
        self._name = name
        self._game_id = game_id
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        # Placeholder for API update
        self._state = 0
        self._attributes = {
            "home_team": "TOR",
            "away_team": "MTL",
            "home": 0,
            "away": 0,
            "shots": {"home": 0, "away": 0},
            "period": 1,
            "time_remaining": "20:00",
            "power_play": {"home": False, "away": False},
        }