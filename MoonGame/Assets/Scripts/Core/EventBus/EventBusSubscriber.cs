using System.Collections.Generic;
using UnityEngine;

namespace Core
{

    /// <summary>
    /// Attach to the same GameObject as event-listening components.
    /// Tracks subscriptions created through this component and automatically
    /// unsubscribes them when the GameObject is destroyed.
    /// Disabled GameObjects remain subscribed.
    /// </summary> 
    [DisallowMultipleComponent]
    public sealed class EventBusSubscriber : MonoBehaviour
    {
        private readonly List<Subscription> _subscriptions = new();

        public Subscription Subscribe<T>(EventListener<T> handler) where T : struct, IEvent
        {
            return Track(EventBus.Subscribe(handler));
        }

        public Subscription Track(Subscription subscription)
        {
            _subscriptions.Add(subscription);
            return subscription;
        }

        public void DisposeAll()
        {
            foreach (var subscription in _subscriptions)
                subscription.Dispose();

            _subscriptions.Clear();
        }

        private void OnDestroy() => DisposeAll();
    }
}
