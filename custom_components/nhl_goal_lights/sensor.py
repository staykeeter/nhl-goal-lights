from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the NHL Goal Lights sensor platform."""
    async_add_entities([NHLGoalSensor(entry)], True)

class NHLGoalSensor(Entity):
    """Sensor to track NHL goals (placeholder)."""

    def __init__(self, entry: ConfigEntry):
        self._entry = entry
        self._state = None
        self._attr_name = "NHL Game Sensor"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch NHL data (replace with live API later)."""
        self._state = "No goals yet"