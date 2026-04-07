import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "nhl_goal_lights"
NHL_TEAMS = [
    "TOR","MTL","BOS","NYR","CHI","DET","CGY","VAN","WPG","EDM",
    "SJS","PHI","PIT","NYI","FLA","COL","DAL","MIN","NSH","STL",
    "CAR","TBL","WSH","ANA","LAK","ARI","VGK","BUF","CBJ","OTT",
    "SEA","NJD"
]

class NHLGoalLightsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Optional("monitor_teams", default=[]): list,
                        vol.Optional("all_games", default=True): bool,
                    }
                ),
            )
        return self.async_create_entry(title="NHL Goal Lights", data=user_input)