# Inventory Domain Rules

Inventory code belongs under `MoonGame/Assets/Scripts/Domains/Inventory/`.

- Put public contracts in `API/`.
- Put implementation details in `Internal/`.
- Put presentation and Unity-facing view code in `UI/`.
- Reference `Core` only.
- Communicate with other domains through Core event-bus events.
