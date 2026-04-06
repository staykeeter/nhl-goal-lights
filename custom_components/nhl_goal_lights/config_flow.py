import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, NHL_TEAMS

class NHLGoalLightsFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="NHL Goal Lights", data=user_input)

        schema = vol.Schema({
            vol.Optional("monitor_teams", default=[]): vol.All(
                vol.List(vol.In(NHL_TEAMS))
            ),
            vol.Optional("all_games", default=False): bool
        })
        return self.async_show_form(step_id="user", data_schema=schema)
