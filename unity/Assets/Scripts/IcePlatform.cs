using UnityEngine;

public class IcePlatform : PlatformBase
{
    
    public float slideMultiplier = 1.5f;

    public override void OnPlayerLanded(PlayerController player)
    {
        player.moveSpeed *= slideMultiplier;
    }

    private void OnCollisionExit2D(Collision2D collision)
    {
        PlayerController p = collision.gameObject.GetComponent<PlayerController>();
        if (p != null)
        {
            p.moveSpeed = PlayerController.instance.moveSpeed; // Reset to default speed
        }
    }
}
