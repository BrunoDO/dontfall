using UnityEngine;

public class BreakablePlatform : PlatformBase
{
    public float breakDelay = 0.15f;

    public override void OnPlayerLanded(PlayerController player)
    {
        Invoke(nameof(Break), breakDelay);
    }

    void Break()
    {
        Destroy(gameObject);
    }
}
