namespace Core
{
    /// <summary>
    /// Handles an event through a readonly reference.
    /// </summary>
    public delegate void EventListener<T>(in T e)
        where T : struct, IEvent;
}
