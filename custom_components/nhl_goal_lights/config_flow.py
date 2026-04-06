from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN

NHL_TEAMS = [
    "ANA","ARI","BOS","BUF","CGY","CAR","CHI","COL","CBJ","DAL",
    "DET","EDM","FLA","LAK","MIN","MTL","NSH","NJD","NYI","NYR",
    "OTT","PHI","PIT","SJS","SEA","STL","TBL","TOR","VAN","VGK","WSH"
]

class NHLGoalLightsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for NHL Goal Lights."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="NHL Goal Lights",
                data={
                    "monitor_teams": user_input.get("monitor_teams", []),
                    "all_games": user_input.get("all_games", True),
                    "wled_devices": user_input.get("wled_devices", [])
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema={
                "monitor_teams": selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=NHL_TEAMS,
                        multiple=True,
                        mode="dropdown"
                    )
                ),
                "all_games": selector.BooleanSelector(),
                "wled_devices": selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="light",
                        multiple=True
                    )
                ),
            },
        )
