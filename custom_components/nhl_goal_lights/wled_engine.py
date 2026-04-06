async def apply_effect(hass, device, step):
    await hass.services.async_call(
        "light",
        "turn_on",
        {
            "entity_id": device,
            "effect": step.get("effect", "Solid"),
            "brightness": step.get("brightness", 255),
        },
        blocking=False,
    )