import aiohttp
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import API_URL, SCAN_INTERVAL

class NHLCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            hass.logger,
            name="nhl",
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as r:
                data = await r.json()
                return data.get("games", [])