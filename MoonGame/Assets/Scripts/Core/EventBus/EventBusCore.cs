using System;
using System.Collections.Generic;

namespace Core
{
    internal sealed class EventBusCore
    {
        private readonly Dictionary<Type, Delegate> _handlers = new();

        /// <summary>
        /// Registers a handler for an event type and returns its subscription handle.
        /// </summary>
        public Subscription Subscribe<T>(EventListener<T> handler) where T : struct, IEvent
        {
            if (handler == null) throw new ArgumentNullException(nameof(handler));

            var eventType = typeof(T);
            if (_handlers.TryGetValue(eventType, out var existing))
                _handlers[eventType] = (EventListener<T>)existing + handler;
            else
                _handlers[eventType] = handler;

            return new Subscription(() => Unsubscribe(handler));
        }

        /// <summary>
        /// Synchronously dispatches an event to a snapshot of its registered handlers.
        /// </summary>
        public void Publish<T>(in T e) where T : struct, IEvent
        {
            if (_handlers.TryGetValue(typeof(T), out var handlers))
                ((EventListener<T>)handlers).Invoke(in e);
        }

        /// <summary>
        /// Removes one matching handler registered for an event type.
        /// </summary>
        public void Unsubscribe<T>(EventListener<T> handler) where T : struct, IEvent
        {
            if (handler == null) return;

            var eventType = typeof(T);
            if (!_handlers.TryGetValue(eventType, out var existing))
                return;

            var remaining = (EventListener<T>)existing - handler;
            if (remaining == null)
                _handlers.Remove(eventType);
            else
                _handlers[eventType] = remaining;
        }

        /// <summary>
        /// Removes all handlers registered for an event type.
        /// </summary>
        public void Clear<T>() where T : struct, IEvent
        {
            _handlers.Remove(typeof(T));
        }

        /// <summary>
        /// Removes all handlers for every event type.
        /// </summary>
        public void ClearAll()
        {
            _handlers.Clear();
        }
    }
}
