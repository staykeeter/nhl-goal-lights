import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import device_registry
from .const import DOMAIN, DEFAULT_WLED_EFFECT, DEFAULT_WLED_BRIGHTNESS, DEFAULT_WLED_SPEED, TEAM_COLORS

WLED_EFFECTS = ["Rainbow", "Color Wipe", "Theater Chase", "Twinkle"]

class NHLGoalLightsOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get all WLED devices from HA device registry
        dev_reg = device_registry.async_get(self.hass)
        wled_devices = [
            (d.id, d.name) for d in dev_reg.devices.values()
            if "wled" in d.manufacturer.lower()
        ]
        wled_dict = {dev_id: name for dev_id, name in wled_devices}

        schema = vol.Schema({
            vol.Optional("wled_device", default=list(wled_dict.keys())[0] if wled_dict else None):
                vol.In(wled_dict),
            vol.Optional("effect", default=DEFAULT_WLED_EFFECT):
                vol.In(WLED_EFFECTS),
            vol.Optional("brightness", default=DEFAULT_WLED_BRIGHTNESS):
                vol.All(int, vol.Range(min=0, max=255)),
            vol.Optional("speed", default=DEFAULT_WLED_SPEED):
                vol.All(int, vol.Range(min=0, max=255)),
            vol.Optional("team_colors", default=TEAM_COLORS):
                dict
        })
        return self.async_show_form(step_id="init", data_schema=schema)