namespace Core
{

    /// <summary>
    /// Global synchronous event bus for publishing and subscribing to struct events.
    /// Events are dispatched immediately to subscribers of the exact event type.
    /// Callers must manage subscription lifetimes and use the bus from the main thread.
    /// </summary>

    public static class EventBus
    {
        private static readonly EventBusCore _global = new();

        public static Subscription Subscribe<T>(EventListener<T> handler)
            where T : struct, IEvent
            => _global.Subscribe(handler);

        public static void Publish<T>(in T e)
            where T : struct, IEvent
            => _global.Publish(in e);

        public static void Unsubscribe<T>(EventListener<T> handler)
            where T : struct, IEvent
            => _global.Unsubscribe(handler);

        public static void Clear<T>()
            where T : struct, IEvent
            => _global.Clear<T>();

        public static void ClearAll()
            => _global.ClearAll();
    }
}
