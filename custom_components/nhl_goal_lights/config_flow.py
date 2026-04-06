from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class NHLGoalLightsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Working config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="NHL Goal Lights",
                data={
                    "all_games": user_input.get("all_games", True),
                    "wled_devices": user_input.get("wled_devices", "")
                }
            )

        schema = vol.Schema({
            vol.Optional("all_games", default=True): bool,
            vol.Optional("wled_devices", default="light.wled_tv"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )
