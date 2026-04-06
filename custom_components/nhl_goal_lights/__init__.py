from .coordinator import NHLCoordinator
from .game_state import GameState
from .event_router import handle_event
from .wled_engine import apply_effect
from .storage import DeviceStore
from .const import DOMAIN

async def async_setup_entry(hass, entry):
    coord = NHLCoordinator(hass)
    await coord.async_config_entry_first_refresh()

    state = GameState()
    store = DeviceStore(hass)
    await store.load()

    hass.data[DOMAIN] = {
        "coord": coord,
        "state": state,
        "store": store,
    }

    async def loop(now):
        games = coord.data
        events = state.update(games)

        devices = list(store.data.keys())

        for e in events:
            await handle_event(hass, e, devices, apply_effect)

    hass.helpers.event.async_track_time_interval(loop, 10)

    return True