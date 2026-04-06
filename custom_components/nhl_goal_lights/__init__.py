import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .coordinator import NHLCoordinator

_LOGGER = logging.getLogger(__name__)

# Store coordinators for each config entry
COORDINATORS = {}

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the integration via YAML (optional, mostly for legacy)."""
    return True  # We use config_flow, so nothing needed here

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up NHL Goal Lights from a config entry."""
    # Get config from UI form
    monitor_teams = entry.data.get("monitor_teams", [])
    all_games = entry.data.get("all_games", True)
    wled_devices = entry.data.get("wled_devices", [])

    # Log what we got
    _LOGGER.info("NHL Goal Lights setup: monitor_teams=%s, all_games=%s, wled_devices=%s",
                 monitor_teams, all_games, wled_devices)

    # Create a coordinator for polling NHL data & managing WLED effects
    coordinator = NHLCoordinator(hass, monitor_teams, all_games, wled_devices)
    await coordinator.async_initialize()

    # Save coordinator for later
    COORDINATORS[entry.entry_id] = coordinator

    # Forward to platforms (if any sensors/lights are created)
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