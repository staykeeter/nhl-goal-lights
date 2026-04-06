from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

NHL_TEAMS = ["ANA","ARI","BOS","BUF","CGY","CAR","CHI","COL","CBJ","DAL",
             "DET","EDM","FLA","LAK","MIN","MTL","NSH","NJD","NYI","NYR",
             "OTT","PHI","PIT","SJS","SEA","STL","TBL","TOR","VAN","VGK","WSH"]

class NHLGoalLightsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title="NHL Goal Lights",
                data={
                    "monitor_teams": user_input["monitor_teams"],
                    "all_games": user_input["all_games"],
                    "wled_devices": user_input["wled_devices"]
                }
            )

        schema = vol.Schema({
            vol.Optional("monitor_teams", default=[]): vol.MultiSelect({t: t for t in NHL_TEAMS}),
            vol.Optional("all_games", default=True): bool,
            vol.Optional("wled_devices", default=[]): vol.Schema([str])
        })

        return self.async_show_form(step_id="user", data_schema=schema)