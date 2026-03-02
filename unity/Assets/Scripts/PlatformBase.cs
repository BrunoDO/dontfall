using UnityEngine;

public class PlatformBase : MonoBehaviour
{
    public virtual void OnPlayerLanded(PlayerController player)
    {
        // Default: do nothing special
    }
}
