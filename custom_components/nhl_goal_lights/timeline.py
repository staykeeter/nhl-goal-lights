import asyncio
import time

async def run_timeline(hass, timeline, devices, apply_effect):
    start = time.time()

    for step in timeline:
        delay = step["t"] - (time.time() - start)
        if delay > 0:
            await asyncio.sleep(delay)

        for device in devices:
            await apply_effect(hass, device, step)