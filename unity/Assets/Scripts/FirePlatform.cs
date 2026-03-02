using UnityEngine;

public class FirePlatform : PlatformBase
{
    public override void OnPlayerLanded(PlayerController player)
    {
        GameManager.instance.EndGame(); // or reduce HP later
    }
}

