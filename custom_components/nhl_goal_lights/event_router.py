from .timeline import run_timeline

GOAL_TIMELINE = [
    {"t": 0, "effect": "Strobe"},
    {"t": 2, "effect": "Color Wipe"},
    {"t": 6, "effect": "Breath"},
]

HAT_TRICK_TIMELINE = [
    {"t": 0, "effect": "Fireworks"},
    {"t": 3, "effect": "Strobe"},
]

async def handle_event(hass, event, devices, apply_effect):
    if event["type"] == "goal":
        await run_timeline(hass, GOAL_TIMELINE, devices, apply_effect)

    if event["type"] == "hat_trick":
        await run_timeline(hass, HAT_TRICK_TIMELINE, devices, apply_effect)