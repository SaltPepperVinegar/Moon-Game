# Core Paradigm

Moon Game uses a simple Core-vs-Domain architecture.

## Project roots

- Unity project root: `MoonGame/`
- Runtime scripts: `MoonGame/Assets/Scripts/`
- Shared code: `MoonGame/Assets/Scripts/Core/`
- Gameplay domains: `MoonGame/Assets/Scripts/Domains/<Domain>/`

## Core

`Core` owns shared infrastructure that every domain is allowed to use. Today that includes the event bus in `MoonGame/Assets/Scripts/Core/EventBus/`; its API and lifecycle rules are documented in `docs/architecture/event_bus.md`.

Core should stay stable, small, and dependency-light. It must not depend on gameplay domains.

## Domains

Each gameplay domain should live in its own folder:

```text
MoonGame/Assets/Scripts/Domains/<Domain>/
  API/
  Internal/
  UI/
  Domain_<Domain>.asmdef
```

The domain assembly definition should reference `Core` by GUID and should not reference other domain assemblies.

## Communication rule

Domains do not call each other directly. If one domain needs to announce something that another domain may care about, publish a `readonly struct` event through the Core event bus.

Event handlers should be scoped by `Subscription` handles. Unity components should either keep and dispose the handle themselves or use `EventBusSubscriber` / `DisposeWith(Component)` so the subscription is cleaned up when the owner is destroyed.

This keeps domain code isolated enough that AI agents and humans can modify one area without accidentally coupling unrelated gameplay systems.
