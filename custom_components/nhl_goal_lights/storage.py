from homeassistant.helpers.storage import Store
from .const import STORE_KEY

class DeviceStore:
    def __init__(self, hass):
        self.store = Store(hass, 1, STORE_KEY)
        self.data = {}

    async def load(self):
        self.data = await self.store.async_load() or {}

    async def save(self):
        await self.store.async_save(self.data)