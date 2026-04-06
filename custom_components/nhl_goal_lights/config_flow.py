import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, NHL_TEAMS

class NHLGoalLightsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for NHL Goal Lights."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="NHL Goal Lights", data=user_input)

        data_schema = vol.Schema({
            vol.Optional("monitor_teams", default=[]): cv.multi_select({t: t for t in NHL_TEAMS}),
            vol.Optional("all_games", default=True): bool,
            vol.Optional("wled_devices", default=[]): cv.multi_select({f"WLED-{i}": f"WLED-{i}" for i in range(1, 5)}),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)
