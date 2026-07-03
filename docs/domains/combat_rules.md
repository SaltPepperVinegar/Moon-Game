# Combat Domain Rules

Combat code belongs under `MoonGame/Assets/Scripts/Domains/Combat/`.

- Put public contracts in `API/`.
- Put implementation details in `Internal/`.
- Put presentation and Unity-facing view code in `UI/`.
- Reference `Core` only.
- Communicate with other domains through Core event-bus events.
