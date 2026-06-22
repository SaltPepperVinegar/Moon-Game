using System;

namespace Core
{
    /// <summary>
    /// Handle for an EventBus registration.
    /// Dispose it when the subscriber no longer needs to receive the event.
    /// </summary>
    public readonly struct Subscription : IDisposable
    {
        private readonly DisposalState _state;

        internal Subscription(Action unsubscribe)
        {
            _state = new DisposalState(unsubscribe);
        }

        public void Dispose() => _state?.Dispose();


        //to avoid _unscribe call repeated while allow subscription to be readonly 
        private sealed class DisposalState
        {
            private Action _unsubscribe;

            public DisposalState(Action unsubscribe)
            {
                _unsubscribe = unsubscribe;
            }

            public void Dispose()
            {
                var unsubscribe = _unsubscribe;
                _unsubscribe = null;
                unsubscribe?.Invoke();
            }
        }
    }
}
