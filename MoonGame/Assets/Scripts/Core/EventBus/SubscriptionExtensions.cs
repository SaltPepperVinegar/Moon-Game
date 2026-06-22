using System;
using UnityEngine;

namespace Core
{
    //extends on Subscription
    public static class SubscriptionExtensions
    {
        /// <summary>
        /// Tracks a subscription and disposes it when the owner's GameObject is destroyed.
        /// </summary>
        public static Subscription DisposeWith(
            this Subscription subscription,
            Component owner)
        {
            if (owner == null)
                throw new ArgumentNullException(nameof(owner));

            var subscriber = owner.GetComponent<EventBusSubscriber>();
            if (subscriber == null)
                subscriber = owner.gameObject.AddComponent<EventBusSubscriber>();

            return subscriber.Track(subscription);
        }
    }
}
