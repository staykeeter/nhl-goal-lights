from homeassistant import config_entries
from homeassistant.helpers import selector
import voluptuous as vol
from .const import DOMAIN

NHL_TEAMS = [
    "ANA","ARI","BOS","BUF","CGY","CAR","CHI","COL","CBJ","DAL",
    "DET","EDM","FLA","LAK","MIN","MTL","NSH","NJD","NYI","NYR",
    "OTT","PHI","PIT","SJS","SEA","STL","TBL","TOR","VAN","VGK","WSH"
]

class NHLGoalLightsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="NHL Goal Lights",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional("monitor_teams"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=NHL_TEAMS,
                        multiple=True,
                    )
                ),
                vol.Optional("all_games", default=True): selector.BooleanSelector(),
                vol.Optional("wled_devices"): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="light",
                        multiple=True
                    )
                ),
            }),
        )
