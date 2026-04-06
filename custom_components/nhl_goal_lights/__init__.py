import logging
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import NHLCoordinator

_LOGGER = logging.getLogger(__name__)
COORDINATORS = {}

async def async_setup(hass: HomeAssistant, config: dict):
    """YAML setup not used; return True for compatibility."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up NHL Goal Lights from a config entry."""
    monitor_teams = entry.data.get("monitor_teams", [])
    all_games = entry.data.get("all_games", True)
    wled_devices = entry.data.get("wled_devices", [])

    _LOGGER.info(
        "Setting up NHL Goal Lights: teams=%s, all_games=%s, wled_devices=%s",
        monitor_teams, all_games, wled_devices
    )

    coordinator = NHLCoordinator(hass, monitor_teams, all_games, wled_devices)
    await coordinator.async_initialize()
    COORDINATORS[entry.entry_id] = coordinator

    # Forward to sensor platform if needed
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    coordinator = COORDINATORS.pop(entry.entry_id, None)
    if coordinator:
        await coordinator.async_shutdown()
    return True
