import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "nhl_goal_lights"
NHL_TEAMS = [
    "TOR","MTL","BOS","NYR","CHI","DET","CGY","VAN","WPG","EDM",
    "SJS","PHI","PIT","NYI","FLA","COL","DAL","MIN","NSH","STL",
    "CAR","TBL","WSH","ANA","LAK","ARI","VGK","BUF","CBJ","OTT",
    "SEA","NJD"
]

class NHLGoalLightsOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(
                    {
                        vol.Optional("effect", default="Flash"): str,
                        vol.Optional("brightness", default=255): int,
                        vol.Optional("speed", default=128): int,
                        vol.Optional(
                            "team_colors",
                            default={t: [255,0,0] for t in NHL_TEAMS}
                        ): dict,
                    }
                ),
            )
        return self.async_create_entry(title="", data=user_input)