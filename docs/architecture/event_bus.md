# Core Event Bus

## Purpose

The Core event bus lets gameplay domains announce facts without directly referencing each other.

Use it when one system needs to publish something that other systems may react to, but the publisher should not know who those listeners are.

## Source files

- Runtime code: `MoonGame/Assets/Scripts/Core/EventBus/`
- Assembly: `MoonGame/Assets/Scripts/Core/Core.asmdef`

## Event shape

Events are value types:

```csharp
public readonly struct PlayerHurtEvent : IEvent
{
    public readonly int Damage;
    public readonly string HitPart;

    public PlayerHurtEvent(int damage, string hitPart)
    {
        Damage = damage;
        HitPart = hitPart;
    }
}
```

Rules:

- Events must be `struct`.
- Events must implement `IEvent`.
- Prefer `readonly struct` for clarity and copy safety.
- Use field names that express gameplay meaning.

## Subscribing

Use `EventBus.Subscribe<T>` for non-Unity lifetimes, or `EventBusSubscriber` / `DisposeWith(Component)` for Unity component lifetimes.

```csharp
private Subscription _hurtSubscription;

private void OnEnable()
{
    _hurtSubscription = EventBus.Subscribe<PlayerHurtEvent>(OnPlayerHurt);
}

private void OnDisable()
{
    _hurtSubscription.Dispose();
}

private void OnPlayerHurt(in PlayerHurtEvent e)
{
    // React to the event.
}
```

For a subscription that should last until the component's GameObject is destroyed:

```csharp
EventBus
    .Subscribe<PlayerHurtEvent>(OnPlayerHurt)
    .DisposeWith(this);
```

Or attach/use `EventBusSubscriber` directly:

```csharp
private EventBusSubscriber _subscriber;

private void Awake()
{
    _subscriber = GetComponent<EventBusSubscriber>();
}

private void Start()
{
    _subscriber.Subscribe<PlayerHurtEvent>(OnPlayerHurt);
}
```

## Publishing

Publish with `in` so large struct events can be passed by readonly reference through the public API.

```csharp
var e = new PlayerHurtEvent(10, "Arm");
EventBus.Publish(in e);
```

Dispatch is synchronous. The handler runs before `Publish` returns.

## Listener delegate

The bus uses this delegate:

```csharp
public delegate void EventListener<T>(in T e)
    where T : struct, IEvent;
```

This is used instead of `Action<T>` because `Action<T>` receives the event by value and copies it when invoked. `EventListener<T>` preserves the `in T` readonly-reference call shape from `Publish` to the listener.

## Lifetime rules

- `Subscription.Dispose()` is idempotent and safe to call more than once.
- Keep the returned `Subscription` if you need manual cleanup.
- Use `DisposeWith(Component)` when the subscription belongs to a Unity component and should be removed on GameObject destruction.
- `EventBusSubscriber` does not unsubscribe on disable. Disabled GameObjects remain subscribed until destroyed or manually disposed.
- Do not leave long-lived global subscriptions pointing at destroyed Unity objects.

## Dispatch behavior

- Events are delivered only to listeners registered for the exact event type.
- There is no inheritance-based event routing.
- There is no queue and no deferred cleanup pass.
- The bus is intentionally synchronous and small.
- Use it from Unity's main thread unless the implementation is explicitly changed later.

## When not to use it

Do not use the event bus for direct ownership, required return values, request/response calls, or tightly coupled logic. If one object must command another specific object, use a direct reference or a domain API instead.
