"""NHL Goal Lights integration."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "nhl_goal_lights"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration via YAML (not used, but required)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up NHL Goal Lights from a config entry."""

    # Store entry data if needed
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward to platforms (like sensors)
    # NOTE: Replace "sensor" with your actual platform(s) if you add them later
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
